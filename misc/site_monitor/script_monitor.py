
# pip install linode_api4
import requests
import smtplib
import os
from linode_api4 import LinodeClient, Instance

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
# Linode-Python-Token
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')

def example_of_connection_to_lenode():
    client = LinodeClient(LINODE_TOKEN)

    def check_out_instances():
        for linode in client.linode.instances():
            print(f'{linode.label}: {linode.id}')

    my_server = client.load(Instance, 000000) # use linode.id from func aboce

    my_server.reboot()

def notify_user():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'YOUR SITE IS DOWN!'
        body = 'Make sure the server restarted and it is back up'
        msg = f'Subject: {subject}\n\n{body}'
        # (SENDER, RECEIVER)
        smtp.sendmail(EMAIL_ADDRESS, 'email@email.com', msg)

def reboot_server():
    client = LinodeClient(LINODE_TOKEN)
    my_server = client.load(Instance, 000000)
    my_server.reboot()

r = requests.get('https://site.com', timeout=5)

if r.status_code != 200:
    notify_user()
    reboot_server()
