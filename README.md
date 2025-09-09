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
2. Install the request module.
   ```bash
   pip install requests
   ```
3. Install the schedule module.
   ```bash
   pip install schedule
   ```
4. Install the DigitalOcean module.
   ```bash
   pip install pydo
   ```
5. Install the OS, dotenv module, which allows saving the ENV variables in an .env file.
   ```bash
   pip install os dotenv
   ```
6. Get the Web status
   ```bash
       try:
        response = requests.get('http://138.197.126.110:8080/')
        print(response.status_code)
   ```
   <img src="" />
  
8. To access Gmail using the application, you must enable 2-step verification and an APP password for your application.
   
10. Check whether the application is running or not. If the application is not running, then the script sends an email notification and restarts the container.
   ```bash
        if response.status_code == 200:
            print("Application is running ok")

        else:
            print("The app is down")

            #Send Email
            msg = f"Subject: SITE DOWN\nFix the issue {response.status_code}"
            send_email(msg)
            # Restart application
            restart_container()
   ```
<img src="" width=800/>

9. In the case that the server is down, then the script restarts the server and container.
    
   ```bash
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
   ```
   <img src="" width=800 />

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
