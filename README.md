# AWSDynamoDBReport
In summary, the code generates a report on DynamoDB tables in the account, detailing their storage class, utilized capacity, region, consumption metrics, scheduled backups, and usage status. This report is then saved as an Excel file.

This code performs a report generation on AWS DynamoDB tables within an account and writes the report to an Excel file. Here's a step-by-step breakdown of the code:

Imports:

The boto3 library is imported for interacting with Amazon Web Services (AWS), particularly DynamoDB.
The pandas library is imported for data manipulation and analysis.
The openpyxl library's Workbook is imported for writing to Excel, although it seems to be unused because the pandas library handles the Excel writing with the xlsxwriter engine.
Initialization:

A Boto3 client for DynamoDB is initialized.
All the DynamoDB tables in the account are listed.
Several lists are initialized to store data for the report. These lists will store information about each table's storage class, utilized capacity, region, read and write capacity units consumed in the last 30 days, scheduled backups, and whether the table is unused.
Data Collection:

For each table in the account, the code performs the following:
Retrieves the table's description.
Extracts the storage class and utilized capacity of the table.
Records the region where the Boto3 client is set up.
Fetches the Read Capacity Units (RCU) and Write Capacity Units (WCU) consumed by the table in the last 30 days.
Lists the scheduled backups for the table.
Determines whether the table is unused based on the consumed RCUs and WCUs.
Data Aggregation:

All the gathered data is aggregated into a Pandas DataFrame. Each list of data becomes a column in the DataFrame.
Export to Excel:

The DataFrame is written to an Excel file named dynamodb_report.xlsx using the xlsxwriter engine.
The Excel writer's book is closed (this finalizes the Excel file).
