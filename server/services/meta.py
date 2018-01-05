class Service:
	def __init__(self, request):
		self.request = request
		self.dbsession = request.dbsession
