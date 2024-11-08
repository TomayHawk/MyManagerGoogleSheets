from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = 'mymanager-service-account.json'
SPREADSHEET_ID = '1cNDmKyyC4IeDrCC4ktwy49Y3PTAZYbvOkjSv_tvUvAw'
RANGE = 'Tasks!A2:Z1000'

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build('sheets', 'v4', credentials=credentials)

def add_task(task_details):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="USER_ENTERED",
        body={'values': task_details}
    ).execute()

def delete_task(task_row):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f'Tasks!A{task_row}:Z{task_row}'
    ).execute()
    deleting_task = result.get('values', [])

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Skipped Tasks!A2',
        valueInputOption="USER_ENTERED",
        body={'values': deleting_task}
    ).execute()

    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 1767357025,
                            "dimension": "ROWS",
                            "startIndex": task_row - 1,
                            "endIndex": task_row
                        }
                    }
                }
            ]
        }
    ).execute()

def return_tasks():
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    print(result.get('values', []))
    return result.get('values', [])

def main():
    while True:
        choice = input("Enter 1 to add a task, '2' to return tasks, '3' to delete a task, and '4' to exit: ")

        if choice == '1':
            add_task([[input("Enter task: "),
                    input("Enter type: "),
                    input("Enter priority: "),
                    input("Enter time required: "),
                    input("Enter time allocation: "),
                    input("Enter deadline: "),
                    "FALSE", # input("Enter completion (TRUE or FALSE): "),
                    input("Enter location: "),
                    input("Enter notification settings: ")]])
        elif choice == '2':
            return_tasks()
        elif choice == '3':
            delete_task(2) ##### 0-index
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
