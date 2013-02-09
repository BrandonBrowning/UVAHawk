
def indexify(items):
	i = 0
	for item in items:
		yield (i, item)

		i += 1