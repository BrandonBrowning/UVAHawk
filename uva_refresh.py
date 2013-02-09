#!/usr/bin/python

import csv

from uva import *

users = user_list()
friday_problems = friday_problem_set()

output_to_html(users, friday_problems)