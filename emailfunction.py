# File: email.py
# From: http://stackoverflow.com/questions/23171140/how-do-i-send-an-email-with-a-csv-attachment-using-python
# Moddified By: Reed S
# Date Mod.: 2014-07-23

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import csv
import os

script_location = os.path.dirname(os.path.realpath(__file__))
location_list = os.listdir(script_location)
email_from = "cdintodb@gmail.com"
email_to1 = "rs7@hawaii.edu"
email_to2 = "aarthi.studio@gmail.com"
username = "cdintodb"
pwd = "energyaudit1!"

def email(email_from, email_to, file_to_send_list, user_name, pwd):
    try:
        print "Sending Message\n"
        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["To"] = email_to
        msg["Subject"] = "Sound Level Meter Data"
        msg.preamble = ""
   
        for file_to_send in file_to_send_list:
            ctype, encoding = mimetypes.guess_type(file_to_send)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(file_to_send)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(file_to_send, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(file_to_send, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(file_to_send, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
            msg.attach(attachment)

            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username, pwd)
            server.sendmail(email_from, email_to, msg.as_string())
            server.quit()
    except Exception, e:
        print "Failed to send Message\n"
        print "Error:\n"
        print e

archive_list = []

with open("archive.csv", "r") as archive_file:
	archive_reader = csv.reader(archive_file, delimiter = ",")
	for archive in archive_reader:
		archive_list.append(archive)

email_filename_list = []
for directory in location_list:
    if str(directory) != "archive.csv" and\
        str(directory) != "emailfunction.py" and\
        str(directory) != "emailfunction.py~" and\
        str(directory) not in archive_list:
            email_filename_list.append(directory)

with open("archive.csv", "wb") as archive_file:
    archive_writer = csv.writer(archive_file, delimiter = ",")    
    for email_filename in email_filename_list:
        output_row = []
        output_row.append(email_filename)
        archive_writer.writerow(output_row)
        
email(email_from, email_to1, email_filename_list, username, pwd)
email(email_from, email_to2, email_filename_list, username, pwd)