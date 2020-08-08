from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.pdfgen import canvas

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'Cred.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1dEFQR-_dQ-VAn6xGi6H5Crj_3gdwnPfLWh_EwgLPvTw'
doc_id = '17CGny5JQdS8qCKwjEyg9b789k4Q2CP6o9QjE6PQcfOo'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='O68:AD100',
    majorDimension='ROWS'
).execute()
# pprint(values)
# print(values['values'])


fileName = 'Konkurs.pdf'
documentTitle = 'Konkurs ishtirokchilari'
title = 'Konkurs ishtirokchilari ro`yxati'
subTitle = 'Konkurs ishtirokchilari ro`yxati (1-100)'

pdf = canvas.Canvas(fileName)
pdf.setTitle(documentTitle)
for value in values['values']:
    print(value)
    pdf.drawCentredString(220, 770, value[0])
    #pdf.line()

pdf.save()
