
import csv
import datetime
import re
import urllib

from uva import *
from bs4 import BeautifulSoup

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

	def __iter__(self):
		for row in self.rows:
			yield row


def next_friday():
	day = datetime.date.today()
	friday = 4

	while day.weekday() != friday:
		day += datetime.timedelta(1)

	return day

def friday_problem_set():
	friday_string = next_friday().strftime("%Y-%m-%d")
	return FancyCsv("config/problems/" + friday_string + ".csv")

def user_map():
	return FancyCsv("config/user_map.csv")

def profile_url(urlid):
	return "http://uva.onlinejudge.org/index.php?option=onlinejudge&Itemid=20&page=show_authorstats&userid=" + str(urlid)

user_name_extract_regex = re.compile("(.*)\s\(.*\)")
def profile_display_name(soup):
	content_headings = soup.find_all("div", class_="contentheading")
	name_login_combo = unicode(content_headings[0].contents[2]).strip()
	name = user_name_extract_regex.match(name_login_combo).groups()[0]

	return name

def profile_solved_displayids(soup):
	rows = soup.find_all("tr", class_="sectiontableentry1") + soup.find_all("tr", class_="sectiontableentry2")

	for row in rows:
		yield int(row.td.a.string)

class UVAUser:
	def __init__(self, urlid):
		url = profile_url(urlid)
		html = urllib.urlopen(url)
		soup = BeautifulSoup(html)

		self.name = profile_display_name(soup)
		self.solved = list(profile_solved_displayids(soup))

def user_list():
	return map(lambda x: UVAUser(x.urlid), user_map())