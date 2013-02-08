#!/usr/bin/python
import csv
import datetime
import urllib
from bs4 import BeautifulSoup
from fancycsv import FancyCsv

def next_friday():
	day = datetime.date.today()
	friday = 4

	while day.weekday() != friday:
		day += datetime.timedelta(1)

	return day

def get_users():
	fancy = FancyCsv("config/user_map.csv")

	for row in fancy.rows:
		yield row

def uva_friday_problems():
	friday_string = next_friday().strftime("%Y-%m-%d")
	fancy = FancyCsv("config/problems/" + friday_string + ".csv")

	for row in fancy.rows:
		yield int(row.problemid)

def uva_profile_url(userid):
	return "http://uva.onlinejudge.org/index.php?option=onlinejudge&Itemid=20&page=show_authorstats&userid=" + str(userid)

def uva_solved_problems(soup):
	rows = soup.find_all("tr", class_="sectiontableentry1") + soup.find_all("tr", class_="sectiontableentry2")

	for row in rows:
		yield int(row.td.a.string)

friday_problems = set(uva_friday_problems())

for user in get_users():
	url = uva_profile_url(user.uvaid)
	page = urllib.urlopen(url)
	soup = BeautifulSoup(page)

	solved_problems = set(uva_solved_problems(soup))

	skipped = friday_problems - solved_problems
	completed = friday_problems & solved_problems

	print("{0} has completed={1} and skipped={2}".format(user.name, list(completed), list(skipped)))
