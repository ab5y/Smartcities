# uncomment to see exceptions and run python -m win32traceutil
import win32traceutil
import win32serviceutil

PORT_TO_BIND = 80
CONFIG_FILE = 'development.ini'
SERVER_NAME = 'www.smartcities.cpr.com'

SERVICE_NAME = 'SmartcitiesWebService'
SERVICE_DISPLAY_NAME = 'Smartcities Web Service'
SERVICE_DESCRIPTION = '''The Smartcities Web Project \
created for CPR by Abhay Sundaram'''

class SCWebService(win32serviceutil.ServiceFramework):
	''' Smartcities Web Service '''

	_svc_name_ = SERVICE_NAME
	_svc_display_name_ = SERVICE_DISPLAY_NAME
	_svc_deps_ = None
	_svc_description_ = SERVICE_DESCRIPTION

	def SvcDoRun(self):
		from cheroot import wsgi
		from pyramid.paster import get_app
		import os, sys

		path = os.path.dirname(os.path.abspath(__file__))

		os.chdir(path)

		app = get_app(CONFIG_FILE)

		self.server = wsgi.Server(
			('0.0.0.0', PORT_TO_BIND),
			app,
			server_name=SERVER_NAME
		)

		self.server.start()

	def SvcStop(self):
		self.server.stop()


if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(SCWebService)