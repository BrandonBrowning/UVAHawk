
class Stub:
	def __init__(self, dict_args=None, **args):
		if dict_args:
			self.__dict__ = dict_args
		else:
			self.__dict__ = args