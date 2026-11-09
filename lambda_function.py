import boto3
import os

ec2 = boto3.client('ec2')
rds = boto3.client('rds')

def lambda_handler(event, context):
    # Action passed from EventBridge payload: "START" or "STOP"
    action = event.get("action", "").upper()
    
    if action not in ["START", "STOP"]:
        print(f"[ERROR] Invalid action parameter: {action}")
        return {"status": "FAILED", "reason": "Invalid action"}
        
    print(f"[INFO] Initiating {action} sequence for tagged resources...")
    
    # -------------------------------------------------------------
    # 1. HANDLE EC2 INSTANCES
    # -------------------------------------------------------------
    ec2_response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Environment', 'Values': ['dev']},
            {'Name': 'tag:Autoshutdown', 'Values': ['True']},
            {'Name': 'tag:Name', 'Values': ['dev-web-server']}
        ]
    )
    
    ec2_ids = []
    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            ec2_ids.append(instance['InstanceId'])
            
    if ec2_ids:
        if action == "STOP":
            ec2.stop_instances(InstanceIds=ec2_ids)
            print(f"[SUCCESS] Stopped EC2 instances: {ec2_ids}")
        elif action == "START":
            ec2.start_instances(InstanceIds=ec2_ids)
            print(f"[SUCCESS] Started EC2 instances: {ec2_ids}")
    else:
        print("[INFO] No matching EC2 instances found to update.")

    # -------------------------------------------------------------
    # 2. HANDLE RDS DATABASES
    # -------------------------------------------------------------
    rds_response = rds.describe_db_instances()
    
    for db in rds_response['DBInstances']:
        db_id = db['DBInstanceIdentifier']
        db_arn = db['DBInstanceArn']
        
        # Check RDS Tags
        tag_list = rds.list_tags_for_resource(ResourceName=db_arn)['TagList']
        tags = {t['Key']: t['Value'] for t in tag_list}
        
        if tags.get('Environment') == 'dev' and tags.get('Autoshutdown') == 'True':
            if action == "STOP" and db['DBInstanceStatus'] == 'available':
                rds.stop_db_instance(DBInstanceIdentifier=db_id)
                print(f"[SUCCESS] Stopping RDS Database: {db_id}")
            elif action == "START" and db['DBInstanceStatus'] == 'stopped':
                rds.start_db_instance(DBInstanceIdentifier=db_id)
                print(f"[SUCCESS] Starting RDS Database: {db_id}")

    return {"status": "SUCCESS", "action": action}