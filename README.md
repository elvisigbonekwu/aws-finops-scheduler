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