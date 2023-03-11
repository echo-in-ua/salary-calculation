from pprint import pprint
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

class Gss():
    """Wrapper for Google SpreadSheet api"""
    def __init__(
        self,
        spreadsheetId=os.environ.get('SPREAD_SHEET_ID'),
        sheetTitle = '2021-07'):
        
        self.credFile = self.createKeyfileDict()
        self.spreadsheetId = spreadsheetId
        self.sheetTitle = sheetTitle
        self.dateFormat = '%Y-%m-%d'
        self.service = self._getService()
        self.sheetId = self._getSheetId(title=sheetTitle)

    def _getService(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credFile,scope)
        
        httpAuth = credentials.authorize( httplib2.Http() )
        service = apiclient.discovery.build( 'sheets', 'v4', http = httpAuth )
        return service

    def createKeyfileDict(self):
        variables_keys = {
            "type": os.environ.get("SHEET_TYPE"),
            "project_id": os.environ.get("SHEET_PROJECT_ID"),
            "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("SHEET_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
            "client_id": os.environ.get("SHEET_CLIENT_ID"),
            "auth_uri": os.environ.get("SHEET_AUTH_URI"),
            "token_uri": os.environ.get("SHEET_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
        }

        return variables_keys

    def writeRows(self, rows, title='2021-07', rowIndex=2 ):
        
        cellsRang=f'A{rowIndex}:I{rowIndex+(len(rows)-1)}'
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = 
        {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": 
            [
                {"range": f"{title}!{cellsRang}",
                 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                 "values": rows     
                }
            ]
        }).execute()
        self._autoFit(title)

    def _autoFit(self,title):
        sheetId = self._getSheetId(title=title)
        results = self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.spreadsheetId, 
            body =
            {
              "requests": [
                {
                  "autoResizeDimensions": {
                    "dimensions": {
                      "sheetId": sheetId,
                      "dimension": "COLUMNS",
                      "startIndex": 0,
                      "endIndex": 9
                    }
                  }
                }
              ]
            }).execute()
    
    def addAndFillNewSheet(self,title):
        if self.addSheet(title=title):
            self.fillNewSheet(title=title)

    def addSheet(self,title) ->bool:
        if not self._sheetPresent(title=title):
            results = self.service.spreadsheets().batchUpdate(
                spreadsheetId = self.spreadsheetId,
                body = 
                {
                  "requests": [
                    {
                      "addSheet": {
                        "properties": {
                          "title": title,
                          "gridProperties": {
                            "rowCount": 50,
                            "columnCount": 14
                          }
                        }
                      }
                    },
                  ]
                }).execute()
            return True
        else: 
            print(f'Sheet with title "{title}" already exists.')
            return False

    def _sheetPresent(self,title):
        return bool(list(filter(lambda sheetsAndTitles:title in sheetsAndTitles, self._sheetsTitlesAndIds() )))

    def fillNewSheet(self, title):
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED",
            "data": 
            [
                {"range": f"{title}!A1:I1",
                 "majorDimension": "ROWS", 
                 "values": [
                                [   
                                    "Дата",
                                    "Працівник",
                                    "Кількість чеків",
                                    "Сумма продажів",
                                    "Сумма знижок",
                                    "Остаточна сумма",
                                    "Середній чек",
                                    "Середня кількість позицій на чек",
                                    "Час запису"
                                ]
                            ]
                }
            ]
        }).execute()

    
    def _getSheetId(self,title) ->int:
        sheetsTitlesAndIds = self._sheetsTitlesAndIds()
        return sheetsTitlesAndIds[title]

    def _sheetsTitlesAndIds(self) ->dict:
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        sheets = sheet_metadata.get('sheets', '')
        sheetsTitlesAndIds = {}
        for sheet in sheets:
            title = sheet.get("properties", {}).get("title", "Sheet1")
            sheetId = sheet.get("properties", {}).get("sheetId", 0)
            sheetsTitlesAndIds[title] = sheetId

        return sheetsTitlesAndIds
    
    def findLastDateAndRowId(self, title='Лист1', cellsRange='A:Z'):
        range = f'{title}!{cellsRange}'
        rows = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=range).execute().get('values', [])
        last_row = rows[-1] if rows else None
        last_row_id = len(rows)
        lastDate = last_row[0]
        lastDate = lastDate if self._isDate(dateString=lastDate) else None
        return (lastDate, last_row_id)

    def _isDate(self, dateString):
        try:
            datetime.strptime(dateString,self.dateFormat)
            return True
        except ValueError as e:
            return False
            print (e)



