from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = 'mymanager-service-account.json'
SPREADSHEET_ID = '1cNDmKyyC4IeDrCC4ktwy49Y3PTAZYbvOkjSv_tvUvAw'
WRITE_RANGE = 'Tasks!A2' # Replace with desired range
READ_RANGE = 'Tasks!A2:C1000' # Replace with desired range

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build('sheets', 'v4', credentials=credentials)

def append_task():
    task_name = input("Enter the task name: ")
    task_time = input("Enter the task time (e.g., 6:30 pm): ")
    task_date = input("Enter the task date (e.g., today or 2024-11-05): ")

    values = [[task_name, task_time, task_date]]
    body = {'values': values}

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=WRITE_RANGE,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells updated.")

# Read values from Google Sheets
def read_tasks():
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=READ_RANGE
    ).execute()

    values = result.get('values', [])

    if not values:
        print("No data found.")
    else:
        print("Task List:")
        for row in values:
            # Assuming each row has task name, time, and date
            print(f"Task: {row[0]}, Time: {row[1]}, Date: {row[2]}")

# Main logic to choose between adding a task and reading tasks
def main():
    choice = input("Enter '1' to add a task or '2' to read tasks: ")

    if choice == '1':
        append_task()
    elif choice == '2':
        read_tasks()
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == '__main__':
    main()
