from google.oauth2 import service_account
import gspread


SERVICE_ACCOUNT_FILE = 'service-account.json'

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
]

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(credentials)
sheet = client.open('Telegram Bot').sheet1

def add_rows(json):

    mylist = list(json.values())

    for value in mylist[-1]:
        val_index = mylist[-1].index(value)
        if value == 1:
            mylist[-1][val_index] = "Вариант №1"
        if value == 2:
            mylist[-1][val_index] = "Вариант №2"
        if value == 3:
            mylist[-1][val_index] = "Вариант №3"

    s = ','.join(mylist[-1])
    mylist[-1] = s
    sheet.append_rows(values=[mylist])
    print("DATA SUCCESSFULLY ADDED TO GOOGLE SHEET")
