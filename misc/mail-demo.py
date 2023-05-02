
import os
import smtplib
import imghdr
from email.message import EmailMessage

# https://myaccount.google.com/security
# https://myaccount.google.com/apppasswords
# https://myaccount.google.com/lesssecureapps

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Subject'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'email@email.com'
msg.set_content('body of email')

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Subject'
    body = 'body of email'
    msg = f'Subject: {subject}\n\n{body}'
    # (SENDER, RECEIVER)
    smtp.sendmail(EMAIL_ADDRESS, 'email@email.com', msg)


# >>> python3 -m smtpd -c DebuggingServer -n localhost:1025
with smtplib.SMTP('localhost', 1025) as smtp:
    # smtp.ehlo()
    # smtp.starttls()
    # smtp.ehlo()
    #
    # smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Subject'
    body = 'body of email'
    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail(EMAIL_ADDRESS, 'email@email.com', msg)

# simpler way to establish connection
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Subject'
    body = 'body of email'
    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail(EMAIL_ADDRESS, 'email@email.com', msg)


# sending to multiple emails
contacts = ['emailTWO@email.com', 'emailONE@email.com']
# different way + sending images
msg = EmailMessage()
msg['Subject'] = 'Subject'
msg['From'] = EMAIL_ADDRESS
msg['To'] = ', '.join(contacts)
msg.set_content('body of email')

# sending images
files = ['pictuer_1.jpg', 'pictuer_2.jpg']
for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)


# for pdf file
files = ['resume.pdf']
for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


# SENDING HTTP
msg = EmailMessage()
msg['Subject'] = 'Subject'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'email@email.com'
msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1></h1>
    </body>
</html>
""", subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
