#!/usr/bin/env python
"""
@author: Rui Miranda
"""
#_______________________________________________________________________________

sleep_req_min = 2
sleep_req_max = 5

participants = [
    dict(
        mail            = 'yourmail@gmail.com',
        name            = 'First Middle Last',
        idNum           = '99999999',
        telNum          = '999999999',
        fbProf          = 'https://www.facebook.com/profileid',
        mail_smtp_pwd   = 'password',
        mail_smtp_srv   = 'smtp.gmail.com:587'
        ),
    dict(
        mail            = 'yourmail@gmail.com',
        name            = 'First Middle Last',
        idNum           = '99999999',
        telNum          = '999999999',
        fbProf          = 'https://www.facebook.com/profileid',
        mail_smtp_pwd   = 'password',
        mail_smtp_srv   = 'smtp.gmail.com:587'
        )
    ]


monitor_page            = 'https://graph.facebook.com/profileid/feed'
monitor_page_auth_param = '?access_token=authToken'
auth_url                = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=app_id&client_secret=app_secret'
auth_app_id             = 'app-id'
auth_app_secret         = 'app-secret'
keyword_uc              = 'CONTEST'

mail_destination    = 'constestmail@com.pt'
mail_subject        = 'CONTEST-NEXTWD3'
mail_body           = """
CONTEST SOMETHING
Name: name
ID: idNum
Contact: telNum
User FB: fbProf
                    """

error_mail              = 'yourmail@gmail.com'
error_mail_smtp_srv     = 'smtp.gmail.com:587'
error_mail_smtp_pwd     = 'password'
