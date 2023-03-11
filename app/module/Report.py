from datetime import date, datetime

class Report():
	"""Wrapper for daily repport. Generate data for record row."""
	def __init__(self, srcData):
		self.srcData = srcData
		self.dateFormat = '%Y-%m-%d'
		self.date = self.setDate()
		self.addDateTimeFormat = '%Y-%m-%d %H:%M:%S'

	def setDate(self):
		return datetime.strptime(self.srcData['date'],self.dateFormat)

	def sheetTitle(self):
		sheetTitleFormat = '%Y-%m'
		return self.date.strftime(sheetTitleFormat)	

	def rows(self) ->list:
	    rows = []
	    for cashier in self.srcData['cashiers']:
	        rows.append(self._row(cashier=cashier))
	    return rows

	def _row(self,cashier):
	    date = self.srcData['date']
	    row = [
	        date,
	        cashier['sales_person_name'],
	        cashier['orders_count'],
	        cashier['sub_total'],
	        cashier['discount_final_amount'],
	        cashier['grand_total'],
	        cashier['average_order_value'],
	        cashier['average_items_per_order'],
	        datetime.now().strftime(self.addDateTimeFormat)
	    ]
	    return row