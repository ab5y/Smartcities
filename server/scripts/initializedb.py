import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import *

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    
    # model = MyModel(name='one', value=1)
    # dbsession.add(model)

    files = ['States', 'Cities', 'Projects', 'SubProjects', 'FinSources', 'Parties']

    import csv
    import psycopg2

    conn = psycopg2.connect("host='localhost' port='5432' dbname='smartcities'")
    curr = conn.cursor()

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print (__location__)
    for file in files:
        with open(__location__ + '\\' + file + '.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row:
                    with transaction.manager:
                        dbsession = get_tm_session(session_factory, transaction.manager)

                        if file == 'States':
                            dbsession.add(State(name=row[0]))

                        elif file == 'Cities':
                            name = row[0]
                            state = dbsession.query(State).filter_by(name=row[1]).first() 
                            dbsession.add(City(name=name, state_id=state.id))

                        elif file == 'Projects':
                            dbsession.add(ProjectCategory(name=row[0]))

                        elif file == 'SubProjects':
                            name = row[0]
                            projectcategory = dbsession.query(ProjectCategory).filter_by(name=row[1]).first()
                            dbsession.add(ProjectSubCategory(name=name, category_id=projectcategory.id))

                        elif file == 'FinSources':
                            dbsession.add(FinanceSource(name=row[0]))

                        elif file == 'Parties':
                            dbsession.add(Party(name=row[0]))
                            
                        # print ', '.join(row)