
body_template_path = "body_template.txt"
output_to_html_path = "output/index.html"

title = "ACMUA SIGCOMP - Leaderboard"
css = ["css/bootstrap.min.css", "css/site.css"]
js = ["js/jquery.min.js"]

def wrap_body_to_html(body):
	def path_to_css_link(path):
		return "<link rel=\"stylesheet\" href=\"{0}\">".format(path)

	def path_to_js_script(path):
		return "<script src=\"{0}\"></script>".format(path)

	css_links = "".join(map(path_to_css_link, css))
	js_scripts = "".join(map(path_to_js_script, js))

	return "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{0}</title>{1}{2}</head><body>{3}</body></html>".format(title, css_links, js_scripts, body)

def bool_to_completed_icon(completed):
	return "<i class=\"{0}\"></i>".format("icon-ok" if completed else "icon-remove")

def generate_problem_completed_table(users, friday_problems):
	def list_to_html_header(items):
		return "<tr>" + "".join(map(lambda x: "<th>" + str(x) + "</th>", items)) + "</tr>"

	def list_to_html_row(items):
		return "<tr>" + "".join(map(lambda x: "<td>" + str(x) + "</td>", items)) + "</tr>"

	header_list = [""] + map(lambda x: "({0.displayid}) {0.name}".format(x), friday_problems)
	header_html = list_to_html_header(header_list)

	# [["<td>{0}</td>".format(user.name)] + [bool_to_completed_icon(problem in user.solved) for problem in friday_problems] for user in users]
	user_completed_list = []
	for user in users:
		user_list = []
		user_list.append(user.name)

		for problem in friday_problems:
			completed = int(problem.displayid) in user.solved
			icon = bool_to_completed_icon(completed)

			user_list.append(icon)

		user_completed_list.append(user_list)

	user_completed_html = "".join(map(list_to_html_row, user_completed_list))
	return "<table class=\"table\">" + "<thead>" + header_html + "</thead>" + "<tbody>" + user_completed_html + "</tbody>" + "</table>"

def winner_text(users, friday_problems):
	best_users = []
	best_solved = 0

	friday_set = set(map(lambda x: int(x.displayid), friday_problems))

	for user in users:
		solved = len(set(user.solved) & friday_set)
		if solved > best_solved:
			best_solved = solved
			best_users = [user.name]

	if best_solved == 0:
		return "Nobody has solved any problems :("

	has_or_have = "has" if len(best_users) == 1 else "have"
	problems_solved = "all of the" if best_solved == len(friday_set) else str(best_solved)
	problems = "problem" + ("s" if best_solved > 1 else "")

	ending = "{0} solved {1} {2}!".format(has_or_have, problems_solved, problems)

	if len(best_users) == 1:
		return best_users[0] + " " + ending
	elif len(best_users) == 2:
		return best_users[0] + " and " + best_users[1] + " " + ending
	else:
		name_csv = ", ".join(best_users)
		last_comma = name_csv.rfind(',')
		return name_csv[:last_comma] + ', and ' + name_csv[last_comma + 2:] + " " + ending

def output_to_html(users, friday_problems):
	table = generate_problem_completed_table(users, friday_problems)

	with open(body_template_path, 'r') as f:
		body = f.read().replace("**TABLE**", table)
		body = body.replace("**WINNER**", winner_text(users, friday_problems))

	with open(output_to_html_path, 'w') as f:
		html = wrap_body_to_html(body)
		f.write(html)