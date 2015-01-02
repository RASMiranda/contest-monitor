#!/usr/bin/env python
"""
@author: Rui Miranda
"""
import traceback, sys
import urllib.request, requests, smtplib
import time, datetime
from email.mime.text import MIMEText
from random import randint

import config
#_______________________________________________________________________________

def send_mail(from_add_r, to_add, subject, body, smtp, smtp_usr, smtp_pwd):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_add_r
    msg['To'] = to_add
    s = smtplib.SMTP(smtp)
    s.starttls()
    s.login(smtp_usr, smtp_pwd)
    s.sendmail(from_add_r, to_add, msg.as_string())
    s.quit()

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def fetchUrl(url):
    f = urllib.request.urlopen(url)
    return f.read()

def get_nextwd(wd):
    d                   = datetime.datetime.now()
    next_thursday       = next_weekday(d, 3) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    next_thursday_day   = next_thursday.strftime('%d').lstrip('0')
    next_thursday_month = next_thursday.strftime('%m').lstrip('0')
    return next_thursday_day + '/' + next_thursday_month

def isWinner(msg, name):
    nameArr = name.split(' ')
    return nameArr[0] in msg and nameArr[-1] in msg

def print_log(log_msg):
    print('['+str(datetime.datetime.now())+'] : '+log_msg)

def sameMessage(last_msg, msg, mail):
    if last_msg:
        if mail in last_msg:
            if last_msg[mail] == msg:
                return True
    return False

def participate(participant):
    subject = config.mail_subject
    if 'NEXTWD' in subject:
        subject = subject[:-7]+get_nextwd(subject[-1:])
    mail_body = config.mail_body\
                    .replace('name', participant['name'])\
                    .replace('idNum', participant['idNum'])\
                    .replace('telNum', participant['telNum'])\
                    .replace('fbProf', participant['fbProf'])
    send_mail(
        participant['mail'],
        config.mail_destination,
        subject,
        mail_body,
        participant['mail_smtp_srv'],
        participant['mail'],
        participant['mail_smtp_pwd'])
    print_log('Sent participation mail from '+participant['mail']+' to '+config.mail_destination)
    time.sleep(randint(1, 3)*0.5)
    send_mail(
        participant['mail'],
        config.mail_destination,
        subject,
        mail_body,
        participant['mail_smtp_srv'],
        participant['mail'],
        participant['mail_smtp_pwd'])
    print_log('Sent participation mail from '+participant['mail']+' to '+config.mail_destination)
    time.sleep(randint(1, 3)*0.5)
    send_mail(
        participant['mail'],
        config.mail_destination,
        subject,
        mail_body,
        participant['mail_smtp_srv'],
        participant['mail'],
        participant['mail_smtp_pwd'])
    print_log('Sent participation mail from '+participant['mail']+' to '+config.mail_destination)


def monitor_cycle(last_msg,url_authToken=None):
    #Retrieve auth token
    if url_authToken:
        authToken = fetchUrl(url_authToken)
        authToken = authToken.decode()
        authToken = authToken.split("=")[1]

    url_json_object = config.monitor_page
    if authToken:
        url_json_object = url_json_object + config.monitor_page_auth_param.replace('authToken',authToken)
    
    json_object = requests.get(url_json_object);

    if 'data' not in json_object.json():
        print(json_object.json())
        print_log('No data in json, sleep 5 seconds...')
        time.sleep(randint(5, 8))
        return
                
    msg     = json_object.json()['data'][0]['message']
    link    = ''
    if 'link' in json_object.json()['data'][0]:
        link = json_object.json()['data'][0]['link']

    for participant in config.participants:
        if config.keyword_uc in msg.upper() and \
           isWinner(msg, participant['name']) and \
           not sameMessage(last_msg, msg, participant['mail']):
            send_mail(
                participant['mail'],
                participant['mail'],
                'WINNER '+config.keyword_uc,
                link,
                participant['mail_smtp_srv'],
                participant['mail'],
                participant['mail_smtp_pwd'])
            print_log('Sent winner mail to '+participant['mail'])
        if config.keyword_uc in msg.upper() and \
           not sameMessage(last_msg, msg, participant['mail']):
            participate(participant)
        if(participant['mail'] and last_msg and msg):
            last_msg[participant['mail']] = msg
    time.sleep(randint(config.sleep_req_min, config.sleep_req_max))
#_______________________________________________________________________________

if __name__ == "__main__":      
    last_msg = dict()

    if config.monitor_page_auth_param:
        url_authToken = config.auth_url\
                           .replace('app_id',config.auth_app_id)\
                           .replace('app_secret',config.auth_app_secret)

    print_log("Started monitor contest "+config.keyword_uc)
    while True:
        try:
            monitor_cycle(last_msg,url_authToken)
        except Exception as e:
            last_msg = None
            excep = traceback.format_exception(*sys.exc_info())
            excep = '\n'.join(excep)
            print_log('(Exception) : '+excep)
            """
            send_mail(
                config.error_mail,
                config.error_mail,
                'Exception '+config.keyword_uc,
                excep,
                config.error_mail_smtp_srv,
                config.error_mail,
                config.error_mail_smtp_pwd)
            """
            #raise e
            continue

    print_log("This should not have ended!")

