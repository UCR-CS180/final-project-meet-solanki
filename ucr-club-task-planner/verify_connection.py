from dotenv import load_dotenv
load_dotenv()
import gspread
import os

client = gspread.service_account(filename="service_account.json")
spreadsheet_name = os.environ.get("SPREADSHEET_NAME", "ucr-club-task-planner")
sheet = client.open(spreadsheet_name).sheet1
print(f"Connected to: {spreadsheet_name}")
print("Header row:", sheet.row_values(1))
print("Row count (data only):", len(sheet.get_all_records()))
print("Connection OK.")
