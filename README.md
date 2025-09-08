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
4. Verify that nginx is accessible

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
5. Install the OS module, which allows saving the ENV variables in an .env file.
   ```bash
   pip install os dotenv
   ```
6. 
## Notification Email
## Restarting Server
   
