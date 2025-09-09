# 🐍Module 14 – Automation with Python
This exercise is part of Module 14: Automation with Python. Module 14 focuses on automating cloud operations with Python. The demos showcase how to interact with AWS services (EC2, EKS, snapshots), perform monitoring tasks, and implement recovery workflows. By the end of this module, you will have practical experience in scripting infrastructure automation, monitoring, and recovery solutions.

# 📦Demo 5 – Website Monitoring and Recovery
# 📌 Objective
 Monitor a website’s availability, send alerts when it is down, and automatically restart the application and server.
 
# 🚀 Technologies Used
* Python: programming language.
* IntelliJ-PyCharm: IDE used for development.
* DigiTalOcean: Cloud provider.

# 🎯 Features
✅ Monitors website via HTTP response
📧 Sends email notifications when downtime occurs
🔄 Automatically restarts the application & server

# Prerequisites
* DigitalOcean account
* Python and PyCharm installed.
  
# 🏗 Project Architecture

# ⚙️ Project Configuration
   
## Deploying DigitalOcean Server
1. Deploy a DigitalOcean Server
2. Install Docker following the guidelines for your OS.
3. Run the nginx Docker container.
   ```bash
   docker run nginx -d -p 8080:80
   ```
4. Verify that nginx is accessible using the IP:Port

## Monitoring the Website
1. Create a new Python file.
2. Install required packages
   ```bash
   pip install requests schedule python-dotenv pydo paramiko
   ```
   <details><summary><strong>Note:</strong></summary>
   * requests = HTTP checks
   * schedule = simple interval scheduling
   * python-dotenv = load .env secrets
   * pydo = DigitalOcean API client
   * paramiko = SSH to restart containers
   * os, smtplib, and time are built-in
 </details>
   
3. Configure environment variables. Create a .env file
   ```bash
    EMAIL_ADDRESS="you@example.com"
    EMAIL_PASSWORD="your_gmail_app_password"
    DIGITALOCEAN_TOKEN="dop_v1_xxx"
   ```
4. To access Gmail using the application, you must enable 2-step verification and an APP password for your application.
   * Enable 2-Step Verification.
   * Create App password
   * Use password as EMAIL_PASSWORD
     
5. Get the Web status
   ```bash
       try:
        response = requests.get('http://138.197.126.110:8080/')
        print(response.status_code)
   ```
   <img src="" />
   
6. Monitoring code: The application monitors the website, restarts the container, and the droplet on host failure.
    ```bash
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
    ```
7. Expected behavior:
    * If the site returns 200, the script returns running OK
    * If the site returns a non-200, it sends a notification email and restarts the container.
    * If the request fails (hots down), it sends an email, reboots the droplet, waits for completion, then restarts the container.

## Notification email
```bash
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # Encrypts communication to our email server
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PWD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_msg)
```

## Restarting Container
```bash
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
 ```
