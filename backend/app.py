# Importing necessary modules
from flask import Flask, request, jsonify
from sql import create_connection, execute_query, execute_insert, execute_update, execute_delete
import traceback
import hashlib

# Initializing Flask app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False
app.config["DEBUG"] = True

# Database configuration
db_config = {
    'hostname': 'cis3368spring.cp0286s66hl9.us-east-2.rds.amazonaws.com',
    'username': 'admin',
    'userpw': 'Cis33682024',
    'dbname': 'Cis3368springdb'
}

# Connection to the database
conn = create_connection(**db_config)

# Valid password for testing login
valid_password = hashlib.sha256('new_password'.encode()).hexdigest()

# Function to check teacher capacity in a given classroom
def check_teacher_capacity(conn, classroom_id):
    query = 'SELECT COUNT(*) FROM child WHERE room = %s'
    values = (classroom_id,)
    result = execute_query(conn, query, values)
    children_count = result[0]['COUNT(*)']
    return children_count < 10

# Helper function to check if a facility with the given id exists
def facility_exists(conn, facility_id):
    query = 'SELECT id FROM facility WHERE id = %s'
    result = execute_query(conn, query, (facility_id,))
    return bool(result)

# Helper function to check if a child with the given id exists
def child_exists(conn, child_id):
    query = 'SELECT id FROM child WHERE id = %s'
    result = execute_query(conn, query, (child_id,))
    return bool(result)

# Helper function to check if a classroom with the given id exists
def classroom_exists(conn, classroom_id):
    query = 'SELECT id FROM classroom WHERE id = %s'
    result = execute_query(conn, query, (classroom_id,))
    return bool(result)

# Helper function to check if adding a child exceeds the class capacity
def check_class_capacity(conn, classroom_id):
    query = 'SELECT COUNT(*) FROM child WHERE room = %s'
    values = (classroom_id,)
    result = execute_query(conn, query, values)
    children_count = result[0]['COUNT(*)']
    return children_count < 10


# Default route
@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to the Daycare Management API!"

# API endpoint for managing facilities
@app.route('/facilities', methods=['GET', 'POST'])
def manage_facilities():
    try:
        if request.method == 'GET':
            query = 'SELECT * FROM facility'
            facilities = execute_query(conn, query)
            return jsonify(facilities)
        elif request.method == 'POST':
            data = request.get_json()
            query = 'INSERT INTO facility (name) VALUES (%s)'
            values = (data['name'],)
            execute_insert(conn, query, values)
            return jsonify({'message': 'Facility added successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/facilities', methods=['PUT'])
def update_facilities():
    try:
        request_data = request.get_json()
        fac_id_update = request_data['id']
        fac_name_update = request_data['name']
        
        # Assuming 'id' is the primary key column in the 'facilities' table
        sql1 = "SELECT id FROM facility WHERE id = %s" % fac_id_update
        newid = execute_query(conn, sql1)[0]["id"]
        
        sql2 = """
        UPDATE facility
        SET name = '%s'
        WHERE id = '%s'
        """ % (fac_name_update, newid)
        
        execute_query(conn, sql2)
        return "Update facility successfully"
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/facilities', methods=['DELETE'])
def delete_facility():
    try:
        request_data = request.get_json()
        facility_id = request_data['id']

        # Assuming 'id' is the primary key column in the 'facilities' table
        sql1 = "SELECT id FROM facility WHERE id = %s " % facility_id
        id = execute_query(conn, sql1, disable_foreign_keys=True)[0]['id']

        sql = "DELETE FROM facility WHERE id = %s" % id
        execute_query(conn, sql, disable_foreign_keys=True)
        return "Deleted Facility successfully"
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500




# API endpoint for managing classrooms
@app.route('/classrooms', methods=['GET', 'POST'])
def manage_classrooms():
    try:
        if request.method == 'GET':
            query = 'SELECT * FROM classroom'
            classrooms = execute_query(conn, query)
            return jsonify(classrooms)
        elif request.method == 'POST':
            data = request.get_json()

            # Check if the provided facility_id exists in the facility table
            facility_id = data.get('facility_id')
            if not facility_exists(conn, facility_id):
                print(f'Invalid facility_id. Facility with id {facility_id} not found.')
                return jsonify({'error': f'Invalid facility_id. Facility with id {facility_id} not found.'}), 400

            # Insert classroom data into the database
            query = 'INSERT INTO classroom (capacity, name, facility_id) VALUES (%s, %s, %s)'
            values = (data['capacity'], data['name'], facility_id)
            execute_insert(conn, query, values)

            return jsonify({'message': 'Classroom added successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

# API endpoint for updating a classroom
@app.route('/classrooms', methods=['PUT'])
def update_classroom():
    try:
        data = request.get_json()
        classroom_id = data.get('id')
        new_name = data.get('name')

        if classroom_id is None or new_name is None:
            return jsonify({'error': 'Classroom ID and Name are required for update'}), 400

        classroom_id = int(classroom_id)

        query = "UPDATE classroom SET name = %s WHERE id = %s"
        values = (new_name, classroom_id)

        execute_query(conn, query, values)

        return jsonify({'message': 'Classroom updated successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/classrooms', methods=['DELETE'])
def delete_classroom():
    try:
        data = request.get_json()
        classroom_id = data['id']

        # Step 1: Delete associated teachers
        delete_teachers_query = "DELETE FROM teacher WHERE room = %s"
        execute_query(conn, delete_teachers_query, (classroom_id,))

        # Step 2: Delete the classroom
        delete_classroom_query = "DELETE FROM classroom WHERE id = %s"
        execute_query(conn, delete_classroom_query, (classroom_id,))

        return jsonify({'message': 'Deleted classroom and associated teachers successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500



# API endpoint for managing teachers
@app.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        query = 'SELECT * FROM teacher'
        teachers = execute_query(conn, query)
        return jsonify(teachers)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/teachers', methods=['POST'])
def manage_teachers():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if 'firstname' not in data or 'lastname' not in data or 'room' not in data:
                return jsonify({'error': 'Missing required fields: firstname, lastname, room'}), 400

            # Check if the provided classroom ID exists in the classroom table
            classroom_id = data['room']
            if not classroom_exists(conn, classroom_id):
                return jsonify({'error': f'Classroom with ID {classroom_id} does not exist'}), 400

            # Insert teacher data into the database
            query = 'INSERT INTO teacher (firstname, lastname, room) VALUES (%s, %s, %s)'
            values = (data['firstname'], data['lastname'], classroom_id)
            execute_insert(conn, query, values)
            return jsonify({'message': 'Teacher added successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500


# API endpoint for managing teachers
@app.route('/teachers', methods=['PUT'])
def update_teacher():
    try:
        data = request.get_json()

        # Check if all required fields are present in the request
        required_fields = ['id', 'firstname', 'lastname', 'room']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Update the teacher in the database
        query = 'UPDATE teacher SET firstname=%s, lastname=%s, room=%s WHERE id=%s'
        values = (data['firstname'], data['lastname'], data['room'], data['id'])
        execute_update(conn, query, values)

        return jsonify({'message': 'Teacher updated successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500



# API endpoint for managing teachers - DELETE
@app.route('/teachers', methods=['DELETE'])
def delete_teacher():
    try:
        data = request.get_json()
        query = 'DELETE FROM teacher WHERE id = %s'
        values = (data['id'],)
        execute_delete(conn, query, values)
        return jsonify({'message': 'Teacher deleted successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500






# Helper function to get the teacher's ID for a given classroom ID
def get_teacher_id_for_classroom(conn, room):
    query = 'SELECT id FROM teacher WHERE room = %s'
    values = (room,)
    result = execute_query(conn, query, values)
    if result:
        return result[0]['id']
    else:
        return None

# Helper function to check if a room with the given id exists
def room_exists(conn, room):
    query = 'SELECT id FROM classroom WHERE id = %s'
    result = execute_query(conn, query, (room,))
    return bool(result)

# Helper function to check if adding a child exceeds the class capacity
def check_teacher_capacity(conn, room):
    query = 'SELECT COUNT(*) FROM teacher WHERE room = %s'
    values = (room,)
    result = execute_query(conn, query, values)
    teacher_count = result[0]['COUNT(*)']
    return teacher_count < 10

@app.route('/children', methods=['GET'])
def get_children():
    try:
        query = 'SELECT * FROM child'
        children = execute_query(conn, query)
        return jsonify(children)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/children', methods=['POST'])
def manage_children():
    try:
        data = request.get_json()
        classroom_id = data.get('room')

        # Check if the classroom exists
        if not classroom_exists(conn, classroom_id):
            return jsonify({'error': f'Classroom with id {classroom_id} does not exist'}), 404

        # Check if adding this child exceeds the class capacity
        if not check_class_capacity(conn, classroom_id):
            return jsonify({'error': 'Classroom is already at maximum capacity'}), 400

        # Check if adding this child exceeds the teacher's capacity
        teacher_id = get_teacher_id_for_classroom(conn, classroom_id)
        if not check_teacher_capacity(conn, teacher_id):
            return jsonify({'error': 'Teacher is already at maximum capacity'}), 400

        # Insert child data into the database
        query = 'INSERT INTO child (firstname, lastname, age, room) VALUES (%s, %s, %s, %s)'
        values = (data['firstname'], data['lastname'], data['age'], classroom_id)
        execute_insert(conn, query, values)
        return jsonify({'message': 'Child added successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/children', methods=['PUT'])
def update_child():
    try:
        data = request.get_json()
        child_id = data.get('id')
        new_room = data.get('room')

        # Check if the child exists
        if not child_exists(conn, child_id):
            return jsonify({'error': f'Child with id {child_id} does not exist'}), 404

        # Check if the new room exists
        if not classroom_exists(conn, new_room):
            return jsonify({'error': f'Classroom with id {new_room} does not exist'}), 400

        # Check if updating this child exceeds the new room's capacity
        if not check_class_capacity(conn, new_room):
            return jsonify({'error': 'Classroom is already at maximum capacity'}), 400

        # Check if updating this child exceeds the teacher's capacity of the new room
        teacher_id = get_teacher_id_for_classroom(conn, new_room)
        if not check_teacher_capacity(conn, teacher_id):
            return jsonify({'error': 'Teacher is already at maximum capacity'}), 400

        # Update child data in the database
        query = 'UPDATE child SET firstname=%s, lastname=%s, age=%s, room=%s WHERE id=%s'
        values = (data['firstname'], data['lastname'], data['age'], new_room, child_id)
        execute_update(conn, query, values)
        return jsonify({'message': 'Child updated successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/children', methods=['DELETE'])
def delete_child():
    try:
        data = request.get_json()
        child_id = data.get('id')

        if child_id is None:
            return jsonify({'error': 'Child ID is required in the request body'}), 400

        query = 'DELETE FROM child WHERE id = %s'
        values = (child_id,)
        execute_delete(conn, query, values)
        return jsonify({'message': f'Child with ID {child_id} deleted successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500



# API endpoint for login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if 'username' in data and 'password' in data:
            if data['username'] == 'admin' and hashlib.sha256(data['password'].encode()).hexdigest() == valid_password:
                return jsonify({'message': 'Login successful'})
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'error': 'Username and password are required'}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
