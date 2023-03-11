class Job():
    """docstring for Job"""
    def __init__(self, gss, title, rows, rowIndex):
        self.gss = gss
        self.title = title
        self.rowIndex = rowIndex
        self.rows = rows
    
    def process(self):
        self.gss.writeRows(rows=self.rows,title=self.title,rowIndex=self.rowIndex)   
    
    def getRows(self) ->list:
        return self.rows
    def getSheetTitle(self) ->str:
        return self.title