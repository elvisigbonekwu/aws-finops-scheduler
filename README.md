# ☁️ AWS FinOps Nightly & Morning Scheduler

An event-driven serverless cloud cost-optimization engine built on AWS that automatically shuts down non-production EC2 instances and RDS databases at night and boots them back up on a morning schedule.

---

## 📌 The Problem
Many organizations leave non-production environments (Development, QA, Staging) running 24/7, burning up to **65% of their monthly cloud budget** on resources that sit completely idle outside of business hours and weekends.

## 🚀 The Solution
This project automates the entire resource lifecycle using a serverless architecture:
* **Automated Nightly Shutdown:** Safely powers down tagged dev resources at 10:00 PM on weekdays.
* **Automated Morning Startup:** Boots resources back up on schedule so they are ready for the team the next day.
* **Cost Savings:** Cuts non-production runtime per month (**~ cost reduction**).

---

## 🏗️ Architecture Overview

```text
[ EventBridge Scheduler ] ──(Cron Triggers: Stop / Start)──> [ AWS Lambda (Python / Boto3) ]
                                                                        │
                        ┌───────────────────────────────────────────────┴───────────────────────────────────────────────v
                        ▼                                                                                               ▼
            [ EC2 Tag Filter: dev / Autoshutdown ]                                                          [ RDS Tag Filter: dev / Autoshutdown ]
                        │                                                                                               │
                        ▼                                                                                               ▼
             (Stops / Starts Instances)                                                                      (Stops / Starts Databases)

## 🛠️ Core Technologies
* **AWS Lambda** (Python 3.12 / Boto3)
* **Amazon EventBridge Scheduler** (Cron-based automated event triggers for START and STOP)
* **AWS IAM** (Least-privilege security roles)
* **Amazon CloudWatch** (Logging and audit trails)

---

## 📋 Prerequisites & Setup

### 1. Resource Tagging
Ensure your target non-production resources are tagged correctly in the AWS Console:
* **EC2 & RDS Tags:**
  * `Environment = dev`
  * `Autoshutdown = True`

### 2. IAM Least-Privilege Policy
Create an IAM execution role for your Lambda function using the policy provided in `iam_policy.json`. It grants explicit access for describing, stopping and starting EC2 and RDS resources, plus CloudWatch logging.

### 3. AWS Lambda Function
* Create a new Lambda function running **Python 3.12**.
* Attach your custom IAM execution role.
* Paste the code from `lambda_function.py` into the inline editor and click **Deploy**.

### 4. EventBridge Schedulers (Nightly & Morning)
Create two separate schedules in **Amazon EventBridge Scheduler** targeting the same Lambda function:

* **Nightly Stop Schedule:**
  * **Cron Expression (10:00 PM weekdays):** `cron(0 22 ? * MON-FRI *)`
  * **Target Payload:** `{"action": "STOP"}`

* **Morning Start Schedule:**
  * **Cron Expression (7:00 AM weekdays):** `cron(0 7 ? * MON-FRI *)`
  * **Target Payload:** `{"action": "START"}`

---

## 🔬 Testing & Verification

* **Manual Test (Lambda Console):** Create test events with `{"action": "STOP"}` and `{"action": "START"}` and click **Test** to verify both state transitions.
* **CloudWatch Audit Logs:** Monitor execution outputs, success flags, and logs under `/aws/lambda/YourFunctionName`.
