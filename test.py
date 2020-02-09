# import psycopg2
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# import datetime
# import secrets
# import time
# import traceback
#
#
# _msg = """xxxcom</a></p>"""
#
# def send_mail(_mail, currentSubject,currentMsg):
#     msg = MIMEMultipart()
#     message = currentMsg
#     username = "python@adsrecognition.com"
#     password = "ASC456ca48ASC89cd"
#     smtphost = "nlss7.a2hosting.com:587"
#     msg["From"] = "python@adsrecognition.com"
#     msg["To"] = _mail
#     msg["Subject"] = currentSubject
#     msg.attach(MIMEText(message, "html"))
#     server = smtplib.SMTP(smtphost)
#     server.starttls()
#     server.login(username, password)
#     server.sendmail(msg['From'], [msg['To'], "no-reply@adsrecognition.com"], msg.as_string())
#     server.quit()
#
#
# send_mail('ankitmahajan478@gmail.com','new Test', 'He new test')
othervar = '%{pts\:gmtime\:1580833680}'
cmd = """ffmpeg -y -i %s -vf drawtext="text='Ch\: %s | Broadcasted at\: %s | ADsrecognition.com - Recordings archive': fontcolor=white: fontsize=38: box=1: boxcolor=black: boxborderw=5: x=30: y=20" -vcodec libx264 -crf 30 -preset veryfast -c:a copy -s 960x540 -codec:a copy -map 0:v -map 0:a -scodec copy -map 0:s -y %s""" %('abc', 'bacd',othervar, 'abc')
print(cmd)