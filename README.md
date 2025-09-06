# 🐍Module 14 – Automation with Python
This exercise is part of Module 14: Automation with Python. Module 14 focuses on automating cloud operations with Python. The demos showcase how to interact with AWS services (EC2, EKS, snapshots), perform monitoring tasks, and implement recovery workflows. By the end of this module, you will have practical experience in scripting infrastructure automation, monitoring, and recovery solutions.

# 📦Demo 5 – Website Monitoring and Recovery
# 📌 Objective
 Monitor a website’s availability, send alerts when it is down, and automatically restart the application and server.
 
# 🚀 Technologies Used
* Python: programming language.
* IntelliJ-PyCharm: IDE used for development.
* AWS: Cloud provider.
* Boto3 AWS SDK for Python.
* Terraform

# 🎯 Features
✅ Monitors website via HTTP response
📧 Sends email notifications when downtime occurs
🔄 Automatically restarts the application & server

# Prerequisites
* AWS account
* Python and PyCharm installed.
* Terraform demo.
  
# 🏗 Project Architecture

# ⚙️ Project Configuration
   
## Creating Snapshots
1. Deploy infrastructure with Terraform
   
2. Import boto3 module.
   ```bash
   import boto3
   ```
   <img src="https://github.com/lala-la-flaca/DevOpsBootcamp_14_Automation_with_Python_2/blob/main/Img/2.PNG" width=800 />
   
3. Import Schedule module
   ```bash
   import schedule
   ```
   <img src="https://github.com/lala-la-flaca/DevOpsBootcamp_14_Automation_with_Python_4/blob/main/Img/3.PNG" width=800 />
   
4. Initialize client
   ```bash
    ec2_client = boto3.client('ec2', region_name="us-east-1")
   ```
    <img src="https://github.com/lala-la-flaca/DevOpsBootcamp_14_Automation_with_Python_4/blob/main/Img/4.PNG" width=800 />
   
