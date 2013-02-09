
import csv
from chickensalad.common import *

def csv_line_stubs(file_handle):
	reader = csv.reader(file_handle)

	for i, line in indexify(reader):
		if i == 0:
			header = line
		else:
			item = Stub(dict(zip(header, line)))
			yield item

class StubCSV:
	def __init__(self, path):
		file_handle = open(path, 'r')
		self.items = list(csv_line_stubs(file_handle))
		file_handle.close()

	def __iter__(self):
		for item in self.items:
			yield item