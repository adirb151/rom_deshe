import json
import logging
import os
import io
import email
import sys
import time
import email.header
import imaplib, re
import smtplib
import mimetypes
import smtplib
from email import encoders
from email.mime import text, base, audio, image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from termcolor import colored
from datetime import datetime
import socket
# from ShellHandler import create_new_target#, run_add_query    ----> DOESNT EXIST
#import ShellHandler


#####################
# account credentials
mail_box = "romgolovin3@gmail.com"#"monagul18@gmail.com"
password = "dmzmezxrhwknprug"#"ouhkvmucqwqwebeh"
# mail_box = os.environ.get("MAIL_BOX")
# password = os.environ.get("PASSWORD")
mail_header = ""  # in dev we want to add a header to indicate that this is a dev message. in prod it should be "".
TAGS = {'start_query': 'NEW', 'update_query': 'UPDATE', 'finish_query': 'DONE'}
SERVER_IP = "localhost"
SERVER_PORT = 5556


def connect(mail_box, password, box="INBOX"):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(mail_box, password)
        result, response = mail.select(box)  # connect to box.
        if result == 'OK':
            logging.info("mail_functions/connect: connecting to " + mail_box + ": " + box + " succeeded")
        else:
            logging.error(
                "mail_functions/connect: failed to connect " + mail_box + "(" + password + "): " + box + " (" + result + ")")
            logging.info(mail.error.args)
            mail.close()
            mail = 0  # couldn't connect to box
        return mail
    except imaplib.IMAP4.error as err:
        logging.error(str(err))
        logging.error("mail_functions/connect: failed to connect " + mail_box + "(" + password + "):")
        return 0  # couldn't connect to mail


def disconnect(mail):
    mail.close()
    mail.logout()


def get_mail(to_disconnect, subject):
    data = {}
    # box = mail_header+ os.environ.get("APP_NAME")
    # logging.info('box = '+box)
    # if os.environ.get("APP_STAGE_NAME"):
    #     box += "_" + os.environ.get("APP_STAGE_NAME")
    # logging.info('box = '+box)
    # mail = connect(box)
    mail = connect(mail_box, password)
    if mail == 0:
        logging.error("can't connect to mailbox!")
    else:
        # logging.info(box + ' connected')
        # bodyCriteria = ' '.join(["BODY \"" + keyword + "\"" for keyword in os.environ.get("BODY_KEYWORDS").split(",")])
        # criteria = '(' + bodyCriteria + ')' # TODO: in real time you should add the field "FROM"
        # logging.info('Createria = '+criteria )
        # result, data_mail = mail.search(None, criteria) # search messages according to the criteria
        result, data_mail = mail.search(None, "UNSEEN FROM me SUBJECT \"", subject, "\"")  # search messages according to the criteria

        logging.info('data_mail length = ' + str(len(data_mail)))
        logging.info('data_mail = ' + str(data_mail[0]))

        if result != 'OK':
            logging.error("error searching messages")
        else:
            #print("##################data_mail#################")
            #print(data_mail)
            #print("############################################")
            for num in data_mail[0].split():
                #print('num = ' + str(num))
                #print(mail.fetch(num, '(UID)'))
                logging.debug('num = ' + str(num))
                result, msg_data = mail.fetch(num, '(RFC822)')  # retrieving the message which it's identifier=num
                if result != 'OK':
                    logging.error("error retrieving message " + num)
                else:
                    # sometimes this step failes on TypeError: 'NoneType' object has no attribute '__getitem__' in this row.
                    # the problem is that it has 2 or more mail in <box> label on gmail.
                    # the solution is to go to this <box> and remove the label.
                    mess = email.message_from_bytes(msg_data[0][1])
                    logging.debug(mess)
                    for part in mess.walk():
                        logging.debug(part)
                        if part.get_content_type() == 'text/plain':
                            buf = part.get_payload()
                            data[num] = buf
        if to_disconnect:
            mail.expunge()
            disconnect(mail)

    return mail, data


def send_mail(subject, msg_body):
    fromaddr = mail_box
    toaddr = mail_box

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = msg_body

    msg.attach(MIMEText(body, 'plain'))

    # filename = "NAME OF THE FILE WITH ITS EXTENSION"
    # attachment = open("PATH OF THE FILE", "rb")

    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload((attachment).read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def create_json(query):
    sub_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    new_query = {
        'tag': TAGS['start_query'],
        'name': 'golrom',
        'data': query,
        'slug': 'temp',
        'status': 'Running',
        'date': sub_date,
        'expiration_date': sub_date,
        'prediction': '',
        'log': ''
    }
    return json.dumps(new_query)


def send_query(json_query):
    sock = socket.socket()
    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)
    sock.sendall(json_query.encode())
    server_msg = sock.recv(1024).decode()
    sock.close()
    return server_msg


def main():
    target = ""
    sequence = ""
    if len(sys.argv) > 1 and sys.argv[1] == '-m':
        target = input("Enter the target:\n").strip()
        sequence = input("Enter the sequence:\n").strip()
        # SIMI LEV GAM PO BE MIKRE SHE ZE YEDANI U NEED TO UPDATEDB!!!
    else:
        subject = "casp-meta"
        mail, data = get_mail(True, subject)
        size = len(list(data.values()))
        if size > 0:
          for data in list(data.values()):
            target = data.split('\r')[0].split('=')[1]
            sequence = data.split('\r')[1].split('=')[1]
            unprocessed_seq = data.split('\r')[1:]
            seq = ''
            for section in unprocessed_seq:
              if '\n' in section:
                section = section.replace('\n','')
              if '=' in section:
                section = section.replace('=','')
              seq += section
            reply_email_index = seq.index("REPLY-E-MAIL")
            sequence = seq[:reply_email_index].replace('SEQUENCE3D','')
            target = target[2:]
            if target != "" and sequence != "":
              print(target)
              print(sequence)
              print()
              # REPLACE
              #open ssh with meshi - add new query (ADD,target, sequence)
              # updateDB(ADD, target, sequence, status="")
              # update cluster DB , folders
        else: 
          print("No new targets.")



if __name__ == '__main__':
    SLEEPING_TIME = 3600 # In seconds
    while True:
      main()
      time.sleep(SLEEPING_TIME)
      
