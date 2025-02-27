from flask import jsonify

def get_employee_route(cursor):
    def get_employee(employee_id):  # Ensure parameter name matches app route
        try:
            query = "SELECT * FROM employees WHERE id = ?"
            result = cursor.execute(query, (employee_id,)).fetchone()
            if result:
                return jsonify({
                    "id": result[0],
                    "name": result[1],
                    "email": result[2],
                    "salary": result[3]
                })
            else:
                return jsonify({"error": "Employee not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return get_employee
