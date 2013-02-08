
import csv

class FancyCsvLine:
    def __init__(self, pairs):
        self.__dict__ = pairs

class FancyCsv:
	def __init__(self, path):
		self.rows = []

		with open(path, 'r') as f:
			reader = csv.reader(f)
			i = 0

			for line in reader:
				if i == 0:
					header = line
				else:
					self.rows.append(FancyCsvLine(dict(zip(header, line))))

				i += 1