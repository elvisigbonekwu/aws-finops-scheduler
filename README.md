# ☁️ AWS FinOps Automated Nightly & Morning Scheduler

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=awslambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![Amazon EventBridge](https://img.shields.io/badge/Amazon-EventBridge-purple?logo=amazonaws&logoColor=white)](https://aws.amazon.com/eventbridge/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, serverless cloud cost-optimization engine built on AWS. This automation utility dynamically discovers, gracefully shuts down and boots up non-production workloads (EC2 instances and RDS databases) based on customized operational schedules, eliminating idle cloud waste.

---

## 📌 The Business Problem
In modern cloud architectures, non-production environments (Development, Testing, Staging) are frequently left running 24/7. When running continuously throughout the month, idle resources consume up to **720 runtime hours**, burning a massive portion of cloud budgets while remaining completely unutilized outside of standard business hours.

## 🚀 The FinOps Solution
This event-driven serverless architecture automates resource state lifecycles to align infrastructure runtime with actual team working hours:
* **Nightly Shutdown:** Automatically halts designated dev workloads at **10:00 PM** on weekdays.
* **Morning Startup:** Automatically wakes workloads back up at **7:00 AM** on weekdays.
* **Quantifiable Impact:** Reduces non-production compute hours from ~720 hours down to ~240 hours per month, delivering an estimated **~66% cost reduction** on target environments.

---

## 🏗️ Architecture & Data Flow

```text
[ EventBridge Scheduler ] ──(Cron Triggers: Stop / Start)──> [ AWS Lambda (Python / Boto3) ]
                                                                        │
                        ┌───────────────────────────────────────────────┴───────────────────────────────────────────────v
                        ▼                                                                                               ▼
            [ EC2 Tag Filter: dev / Autoshutdown ]                                                          [ RDS Tag Filter: dev / Autoshutdown ]
                        │                                                                                               │
                        ▼                                                                                               ▼
             (Stops / Starts Instances)                                                                      (Stops / Starts Databases)

Core Technologies
Compute Engine: AWS Lambda (Python 3.12 utilizing Boto3 SDK)

Trigger/Orchestration: Amazon EventBridge Scheduler (Cron expressions with custom JSON payloads)

Security & Access Control: AWS IAM (Least-privilege security policy implementation)

Observability & Auditing: Amazon CloudWatch Logs (Centralized execution tracking and log streams)

📂 Repository Structure

```text
aws-finops-scheduler/
│
├── lambda_function.py       # Core automation script handling EC2 and RDS state transitions
├── iam_policy.json          # Least-privilege IAM permissions document
└── README.md                # Comprehensive deployment and architecture guide

📋 Comprehensive Deployment & Setup Guide

Follow these steps to deploy the entire automation engine into your AWS account from scratch.

Step 1: Resource Tagging StrategyThe engine utilizes resource-based tagging to safely target non-production assets without hardcoding identifiers.

- Navigate to the EC2 Console or RDS Console.
- Select your target dev resource and assign the following tags:
~ Key: Environment | Value: dev
~ Key: Autoshutdown | Value: True

Step 2: Create the IAM Execution RoleTo give your Lambda function permissions to manage your EC2 instances, RDS databases, and CloudWatch logs:
- Open the IAM Console > Roles > Create role.
- Select AWS service as the trusted entity type, and choose Lambda as the service.
- Attach the necessary permissions (using the permissions from iam_policy.json or selecting the required EC2/RDS/CloudWatch actions during creation).
- Attach the AWS managed policy AWSLambdaBasicExecutionRole so it can write logs to CloudWatch.
- Name the role AutoSchedulerExecutionRole and complete creation.

Step 3: Deploy the AWS Lambda Function
- Navigate to the AWS Lambda Console > Click Create function.
- Choose Author from scratch:
~ Function name: AutoSchedulerEngine
~ Runtime: Python 3.12
~ Architecture: x86_64 (or arm64)
~ Execution role: Select Use an existing role and choose AutoSchedulerExecutionRole.
-Click Create function.
- In the code editor, paste the contents of lambda_function.py.
- Click Deploy to save changes.

Step 4: Configure EventBridge Schedulers (Nightly & Morning)
Create two separate event schedules in Amazon EventBridge Scheduler targeting your Lambda function.
1. Nightly Stop Schedule:
- Name: Nightly-Stop-NonProdSchedule 
- type: Recurring schedule (Cron-based)
- Cron Expression (10:00 PM weekdays): cron(0 22 ? * MON-FRI *)
- Target API: AWS Lambda > InvokeLambda 
- Function: AutoSchedulerEngine
- Payload (JSON):
   { "action": "STOP" }

2. Morning Start Schedule:
- Name: Morning-Start-NonProdSchedule 
- type: Recurring schedule (Cron-based)
- Cron Expression (7:00 AM weekdays): cron(0 7 ? * MON-FRI *)
- Target API: AWS Lambda > InvokeLambda 
- Function: AutoSchedulerEngine
- Payload (JSON):
{ "action": "START" }

🔬 Testing & Validation
1. Manual Dry-Run (Lambda Console):
- Go to the Test tab in your Lambda function.
- Create a test event named TestStop with payload: {"action": "STOP"} and click Test.
- Repeat with {"action": "START"} to verify state restoration.

2. Observability & CloudWatch Audit Logs:
- Navigate to Amazon CloudWatch > Log groups > /aws/lambda/AutoSchedulerEngine.
- Review execution output streams to confirm successful resource filtering and state flags ([SUCCESS] Stopped EC2 instances...).

🤝 Contributing & Feedback
Contributions, issues, and feature requests are welcome! Feel free to check issues or submit a pull request.