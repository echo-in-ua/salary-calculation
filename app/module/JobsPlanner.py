from .Job import Job
from .Report import Report
from datetime import date, datetime, timedelta

class JobsPlanner():
    def __init__(self,gss,api) -> None:
        self.gss=gss
        self.dateFormat = '%Y-%m-%d'
        self.api = api
        self.workSheetTitle = self._setSheetTitle()
        self._checkIfSheetExistAndCreate()
        self.firstRowId = 2

    def _checkIfSheetExistAndCreate(self) ->None:
        self.gss.addAndFillNewSheet(title=self.workSheetTitle)    

    def _setSheetTitle(self) ->None:
        now = datetime.now()
        sheetTitleFormat = '%Y-%m'
        return now.strftime(sheetTitleFormat)

    def _datesInPeriod(self,firstDay, lastDay) ->list:
        now = datetime.now()
        dates=[]
        for dayNumber in range(firstDay,lastDay+1):
            day = date(now.year,now.month,dayNumber)
            dates.append(day.strftime(self.dateFormat))
        return dates    

    def _datesFromFirstMonthDay(self) ->list:
        now = datetime.now()
        firstDay = 1
        lastDay = now.day
        return self._datesInPeriod(firstDay=firstDay,lastDay=lastDay)
    
    def _datesFromLastRecord(self) ->list:
        now = datetime.now()
        dates = []
        lastRecordDayStr, lastRecordRowId = self._findLastRecordDayNumber()
        if lastRecordDayStr is None:
            firstDayDate = datetime.today().replace(day=1)
        else:
            firstDayDate = datetime.strptime(lastRecordDayStr,self.dateFormat)+timedelta(days=1)
        firstDay = firstDayDate.day
        self.firstRowId = lastRecordRowId + 1
        lastDay = now.day
        return self._datesInPeriod(firstDay=firstDay,lastDay=lastDay)
    
    def _findLastRecordDayNumber(self) ->tuple:
        title = self.workSheetTitle
        dateStr, rowId = self.gss.findLastDateAndRowId(title)
        return (dateStr, rowId)
    
    def jobs(self) ->list:
        jobs = []
        dates = self._datesFromLastRecord()
        index=self.firstRowId
        for date in dates:
            report = Report(self.api.fetch_data(date))
            sessionCount = len(report.rows())
            jobs.append(Job(gss=self.gss, title=report.sheetTitle(),rows=report.rows(),rowIndex=index))
            index += sessionCount
        return jobs

    def run(self) ->None:
        for job in self.jobs():
            job.process()

    def butchRun(self) ->None:
        batch = []
        index = 2
        for job in self.jobs():
            for row in job.getRows():
                batch.append(row)
        title = self.workSheetTitle
        batchJob = Job(gss=self.gss, title=title,rows=batch,rowIndex=index)
        batchJob.process()