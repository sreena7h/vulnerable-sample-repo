from flask import Flask
from routes.get_employee import get_employee_route
from routes.add_employee import add_employee_route
from routes.list_employee import list_employees_route
from db.initialize import initialize_database, create_tables
from telemetry_agent import telemetry_initialize


app = Flask(__name__)
connector = initialize_database()
cursor = connector.cursor()
telemetry_initialize()
create_tables(cursor, connector)

# Register routes
app.add_url_rule('/employees/<int:employee_id>', view_func=get_employee_route(cursor), strict_slashes=False)
app.add_url_rule('/create-employee', view_func=add_employee_route(cursor, connector),
                 methods=['POST'], strict_slashes=False)
app.add_url_rule('/employees', view_func=list_employees_route(cursor), methods=['GET'], strict_slashes=False)

if __name__ == '__main__':
    app.run(debug=True)
