import json

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import *
from ..services import ProjectService

@view_config(route_name='home', renderer='../templates/home.jinja2')
def my_view(request):
    try:
        pass
        # query = request.dbsession.query(MyModel)
        # one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': 'one', 'project': 'server'}

@view_config(route_name='cities', renderer='../templates/cities.jinja2')
def cities(request):
    try:
        query = request.dbsession.query(City)
        cities_li = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'cities': cities_li}

@view_config(route_name='projects', renderer='../templates/projects.jinja2')
def projects(request):
    try:
        dataProjects = ProjectService(request).get_projects_treemap_json()
        dataPhases = ProjectService(request).get_phases_treemap_json()
        dataStates = ProjectService(request).get_states_treemap_json()
        dataCities = ProjectService(request).get_cities_treemap_json()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {
                'data_projects': json.dumps(dataProjects),
                'data_phases': json.dumps(dataPhases),
                'data_states': json.dumps(dataStates),
                'data_cities': json.dumps(dataCities)
            }

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_server_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
