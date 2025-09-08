import time
import requests
import smtplib
from dotenv import  load_dotenv
import  paramiko
import os
import pydo
import schedule


#Getting ENV Variables from .env file
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PWD = os.getenv("EMAIL_PASSWORD")
DO_TOKEN = os.getenv("DIGITALOCEAN_TOKEN")

def send_email(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # Encrypts communication to our email server
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PWD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_msg)


def restart_container():
    print("Restarting Application Container...")
    ssh = paramiko.SSHClient()
    # AutoAddPolicy automatically allows the connection to the server
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="138.197.126.110", username='root', key_filename='/home/lala/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start e76048d7c881')
    print(stdout.readlines())
    ssh.close()
    print("Application restarted")


def monitoring_app():
    try:
        response = requests.get('http://138.197.126.110:8080/')
        print(response.status_code)

        if response.status_code == 200:
            print("Application is running ok")

        else:
            print("The app is down")

            #Send Email
            msg = f"Subject: SITE DOWN\nFix the issue {response.status_code}"
            send_email(msg)
            # Restart application
            restart_container()

    except Exception as ex:
        print(f"Connection Error happened: {ex}")
        # Send Email
        msg = f"Subject: SITE DOWN\n application is not accessible"
        send_email(msg)

        #Restart DO droplet
        print("Rebooting The server:")
        do_client = pydo.Client(DO_TOKEN)
        do_list =  do_client.droplets.list(tag_name="nginx-server")
        do_id = do_list['droplets'][0]['id']
        #print(do_id)
        #print(do_list)

        req = {
            "type": "reboot"
        }
        reboot_res =  do_client.droplet_actions.post(droplet_id=do_id, body=req)
        #print(f"Reboot Response: {reboot_res}")

        # Reboot Status Check
        reboot_action_id = reboot_res["action"]["id"]

        while True:
            action_response = do_client.droplet_actions.get(droplet_id=do_id, action_id= reboot_action_id)
            action= action_response["action"]['status']
            print(f"Reboot status: {action}")
            if action == 'completed':
                time.sleep(20)
                print("Reboot completed.Starting application")
                restart_container()
                break


schedule.every(10).seconds.do(monitoring_app)

while True:
    schedule.run_pending()

