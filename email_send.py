from utilities.utility import *
import smtplib

utilization_directory = 'safe_directory/'
config = read_config_ini(utilization_directory+"dbconfig.ini")

gmail_user = config['GMAIL']['email']
gmail_password = config['GMAIL']['password']

sent_from = gmail_user  
to = ['smazoomder@gmail.com']
subject = 'Activate Account - ROBIST'
body = "Hey, thanks for register with Robist account. To activate your account, click here or visit this link - .\n\n- You"
CC = ''

subject_ = ''.format(subject)
email_text = f"""Subject: {subject}
From: {sent_from}
To: {", ".join(to)}
CC: {CC}

{body}
"""
email_text = subject_ + email_text
try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')

except:  
    print('Something went wrong...')