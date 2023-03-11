from module.Daily_sales_report_api import Daily_sales_report_api
from module.Gss import Gss
from module.Report import Report
from module.JobsPlanner import JobsPlanner
from os import environ
from datetime import date, datetime, timedelta
import pprint

def getReport():
    pprint.pprint ( environ.get('API_HOST_NAME') )
    pprint.pprint ( environ.get('API_AUTH') )
    
    api_host = environ.get('API_HOST_NAME')
    api_auth = environ.get('API_AUTH')
    report_date = '2021-07-06'
    api = Daily_sales_report_api( api_host=api_host, auth=api_auth, report_date_str=report_date )

    report = api.fetch_data()
    pprint.pprint ( report )
    return report

def app():
    api_host = environ.get('API_HOST_NAME')
    api_auth = environ.get('API_AUTH')
    spreadsheetId = environ.get('SPREAD_SHEET_ID')
    startPeriod = environ.get('START_PERIOD')
    gss = Gss(spreadsheetId = spreadsheetId, sheetTitle = startPeriod)

    api = Daily_sales_report_api( api_host=api_host, auth=api_auth)
    jp = JobsPlanner(gss=gss,api=api)
    jp.run()
         
if __name__ == '__main__':
    app()

