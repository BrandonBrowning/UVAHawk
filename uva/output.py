
import datetime
from uva import *

body_template_path = "body_template.html"
output_html_path = "output/index.html"
output_last_modified_path = "output/last_modified.json"

title = "ACMUA SIGCOMP - Leaderboard"
css = ["css/bootstrap.min.css", "css/font-awesome.min.css", "css/site.css"]
js = ["js/jquery.min.js", "http://d3js.org/d3.v3.min.js", "js/site.js"]

def wrap_body_to_html(body):
	def path_to_css_link(path):
		return "<link rel=\"stylesheet\" href=\"{0}\">".format(path)

	def path_to_js_script(path):
		return "<script src=\"{0}\"></script>".format(path)

	css_links = "".join(map(path_to_css_link, css))
	js_scripts = "".join(map(path_to_js_script, js))

	return "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{0}</title>{1}{2}</head><body>{3}</body></html>".format(title, css_links, js_scripts, body)

def bool_to_completed_icon(completed):
	return "<i class=\"{0} icon-3x\"></i>".format("icon-ok" if completed else "icon-remove")

def friday_problems_to_table_header(friday_problems):
	cells = []
	cells.append("")

	for problem in friday_problems:
		cells.append("<a href=\"{0}\">{1.displayid} - {1.name}</a>".format(problem_url(problem.urlid), problem))

	cells_html = map(lambda cell: "<th>{0}</th>".format(cell), cells)
	return "<tr>{0}</tr>".format("".join(cells_html))

def user_to_table_row(user, friday_problems):
	cells = []
	cells.append("<h3><a href=\"{0}\">{1}</a></h3>".format(profile_url(user.urlid), user.name))
	for problem in friday_problems:
		completed = int(problem.displayid) in user.solved
		icon = bool_to_completed_icon(completed)

		cells.append(icon)

	cells_html = map(lambda cell: "<td>{0}</td>".format(cell), cells)
	return "<tr>{0}</tr>".format("".join(cells_html))
	

def generate_problem_completed_table(users, friday_problems):
	header_html = friday_problems_to_table_header(friday_problems)

	users_completed = [(u, u.completed(friday_problems)) for u in users]
	users_sorted = [t[0] for t in sorted(users_completed, reverse=True, key=lambda x: x[1])]

	user_html = "".join(map(lambda user: user_to_table_row(user, friday_problems), users_sorted))

	return "<table class=\"table\"><thead>{0}</thead><tbody>{1}</tbody></table>".format(header_html, user_html)

def winner_text(users, friday_problems):
	best_users = []
	best_solved = 0

	friday_set = set(map(lambda x: int(x.displayid), friday_problems))

	for user in users:
		solved = len(set(user.solved) & friday_set)

		if solved == best_solved:
			best_users.append(user.uva_name)
		elif solved > best_solved:
			best_solved = solved
			best_users = [user.uva_name]

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

	with open(output_last_modified_path, 'w') as f:
		f.write("\"{0}\"".format(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))

	with open(output_html_path, 'w') as f:
		html = wrap_body_to_html(body)
		f.write(html)