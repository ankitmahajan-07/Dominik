import psycopg2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
from email.message import EmailMessage

_msg = """xxxcom</a></p>"""

def send_mail(_mail, currentSubject,currentMsg):
    try:
        msg = MIMEMultipart()
        message = currentMsg
        username = "python@adsrecognition.com"
        password = "ASC456ca48ASC89cd"
        smtphost = "nlss7.a2hosting.com:587"
        msg["From"] = "python@adsrecognition.com"
        msg["To"] = _mail
        msg["Subject"] = currentSubject
        msg.attach(MIMEText(message, "html"))
        server = smtplib.SMTP(smtphost)
        server.starttls()
        server.login(username, password)
        server.sendmail(msg['From'], [msg['To'], "no-reply@adsrecognition.com"], msg.as_string())
        print('Sent mail successfully')
    except:
        print('Unable to send mail')
    finally:
        server.quit()


connection = psycopg2.connect(user="verifyrecordsaccess",
                                      password="SLZHyyk39lABeL3i",
                                      host="164.68.97.194",
                                      port="",
                                      database="recognition_audiofinger4sec")

cursor = connection.cursor()
# Print PostgreSQL Connection properties
print(connection.get_dsn_parameters(), "\n")

# Print PostgreSQL version
oldStatus = {}
oldRecordLength = 0
j=0
while True:
    query = "SELECT * from alive"
    cursor.execute(query)
    records = list(cursor.fetchall())

    print(records)

    if len(records) > oldRecordLength:
        oldRecordLength = len(records)
        j=0

    for record in records:
        if j==0:
            oldStatus[record[1]] = record[-2]
        if record[-2] == 'Connected':
            dateTime = record[2]
            for i in range(0,3):
                newquery = 'select lastalive from alive where radiochannel_id=%s'
                cursor.execute(newquery,[record[0]])
                newLastAlive = cursor.fetchone()
                if newLastAlive != None:
                    if dateTime == newLastAlive[0]:
                        if i < 2:
                            time.sleep(15)
                            continue
                        else:
                            print("Connection is not being updated, Sending error mail!!")
                            try:
                                send_mail('no-reply@adsrecognition.com',
                                          'Audio ' + record[1] + ' ' + record[-1] + ' NOT ALIVE',
                                          'Error alert')
                            except:
                                print(
                                    'Make sure you have allowed less secure apps functionality on your email account.')
                    else:
                        print(record[1] + ' is still connected.')
                        break
        else:
            if record[-2] == 'Unconnected' or record[-2] == 'Error':
                print(record[1] + ' ' + record[-1] + ' has lost connection with server. Sending Mail')
                try:
                    send_mail('no-reply@adsrecognition.com',
                              'Audio ' + record[1] + ' ' + record[-1] + ' has lost connection',
                              'Error alert')
                except:
                    print('Make sure you have allowed less secure apps functionality on your email account.')
            else:
                print(record[1] + ' ' + record[-1] + ' has been terminated. Sending Mail')
                try:
                    send_mail('no-reply@adsrecognition.com',
                              'Audio ' + record[1] + ' ' + record[-1] + ' has been terminated',
                              'Error alert')
                except:
                    print('Make sure you have allowed less secure apps functionality on your email account.')

    time.sleep(3)
    j+=1

