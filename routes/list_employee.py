from flask import jsonify

def list_employees_route(cursor):
    def list_employees():  # Renamed from `route`
        try:
            query = "SELECT * FROM employees"
            employees = cursor.execute(query).fetchall()

            return jsonify([
                {
                    "id": emp[0],
                    "name": emp[1],
                    "email": emp[2],
                    "salary": emp[3]
                } for emp in employees
            ])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return list_employees  # Return `list_employees`
