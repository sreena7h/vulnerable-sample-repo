from flask import request, jsonify

def add_employee_route(cursor, conn):
    def route():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            salary = data.get('salary')

            if not name or not email or not salary:
                return jsonify({"error": "Missing required fields."}), 400

            query = f"INSERT INTO employees (name, email, salary) VALUES ('{name}', '{email}', {salary})"
            cursor.execute(query)
            conn.commit()

            return jsonify({"message": "Employee added successfully."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return route
