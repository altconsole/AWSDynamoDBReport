import boto3
import pandas as pd
from openpyxl import Workbook

# Initialize the Boto3 DynamoDB client
client = boto3.client('dynamodb')

# Retrieve a list of all DynamoDB tables in the account
table_list = client.list_tables()['TableNames']

# Initialize lists to store the data we want to report
storage_classes = []
utilized_capacity = []
regions = []
rcu_consumed = []
wcu_consumed = []
scheduled_backups = []
unused = []  # New list to store information about unused tables

# Loop through each table and retrieve the data we want to report
for table_name in table_list:
    # Retrieve the table description
    table_desc = client.describe_table(TableName=table_name)['Table']
    
    # Retrieve the storage class and utilized capacity
    storage_classes.append(table_desc['BillingModeSummary']['BillingMode'])
    utilized_capacity.append(table_desc['TableSizeBytes'] / 1024 / 1024 / 1024)
    
    # Retrieve the region
    regions.append(client.meta.region_name)
    
    # Retrieve the RCU and WCU consumed in the last 30 days
    rcu_stats = client.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedReadCapacityUnits',
        Dimensions=[
            {'Name': 'TableName', 'Value': table_name}
        ],
        StartTime=pd.Timestamp('30 days ago').isoformat(),
        EndTime=pd.Timestamp.now().isoformat(),
        Period=86400,
        Statistics=['Sum']
    )
    if rcu_stats['Datapoints']:
        rcu_consumed.append(rcu_stats['Datapoints'][0]['Sum'])
    else:
        rcu_consumed.append(0)
    
    wcu_stats = client.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedWriteCapacityUnits',
        Dimensions=[
            {'Name': 'TableName', 'Value': table_name}
        ],
        StartTime=pd.Timestamp('30 days ago').isoformat(),
        EndTime=pd.Timestamp.now().isoformat(),
        Period=86400,
        Statistics=['Sum']
    )
    if wcu_stats['Datapoints']:
        wcu_consumed.append(wcu_stats['Datapoints'][0]['Sum'])
    else:
        wcu_consumed.append(0)
    
    # Retrieve the list of scheduled backups for the table
    backup_list = client.list_backups(TableName=table_name)['BackupSummaries']
    if backup_list:
        scheduled_backups.append(', '.join([backup['BackupArn'] for backup in backup_list]))
    else:
        scheduled_backups.append('No scheduled backups')
    
    # Determine if the table is unused
    if rcu_consumed[-1] == 0 and wcu_consumed[-1] == 0:
        unused.append('Unused')
    else:
        unused.append('Used')

# Create a Pandas DataFrame to store the data
data = {
    'Table Name': table_list,
    'Storage Class': storage_classes,
    'Utilized Capacity (GB)': utilized_capacity,
    'Region': regions,
    'RCU Consumed (Last 30 Days)': rcu_consumed,
    'WCU Consumed (Last 30 Days)': wcu_consumed,
    'Scheduled Backups': scheduled_backups,
    'Unused Tables': unused  # Adding the new column
}
df = pd.DataFrame(data)

# Write the DataFrame to an Excel spreadsheet
writer = pd.ExcelWriter('dynamodb_report.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False)
writer.book.close()
