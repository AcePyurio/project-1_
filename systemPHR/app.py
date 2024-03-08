import base64
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mysql.connector
import jwt
import datetime
import hashlib
import secrets
from http import HTTPStatus


# Secret key for JWT token signing
SECRET_KEY = "your_secret_key_here"

def connect_to_database():
    return mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306", database='db'
    )

# Function to hash the password
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password, salt

# Function to authenticate the user using Basic authentication
def basic_authenticate(username, password):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        stored_password, salt = user[2], user[3]
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        if hashed_password == stored_password:
            return user[0]  # Return user_id if password is correct

    return None

# Function to generate JWT token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to authenticate the user using Bearer authentication
def bearer_authenticate(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
    
        connection = connect_to_database()
        cursor = connection.cursor()


        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()


        cursor.close()
        connection.close()

  
        return user is not None
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Invalid token
        return False

# Function to handle user registration
def register_user(username, password, email, first_name, last_name):

    hashed_password, salt = hash_password(password)

    connection = connect_to_database()
    cursor = connection.cursor()
 
    query = "INSERT INTO users (username, password, salt, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (username, hashed_password, salt, email, first_name, last_name))
    connection.commit()

    cursor.close()
    connection.close()


def add_health_record(patient_id, date, diagnosis, treatment, medical_condition, family_history, healthcare_provider):
    try:
      
        connection = mysql.connector.connect(
            user='root', password='root', host='mysql', port="3306", database='db'
        )
        
        cursor = connection.cursor()
        
        
        insert_query = """
        INSERT INTO health_records (patientID, date, diagnosis, treatment, medicalcondition, familyhistory, healthcareprovider)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
       
        cursor.execute(insert_query, (patient_id, date, diagnosis, treatment, medical_condition, family_history, healthcare_provider))
        
       
        connection.commit()
        
       
        cursor.close()
        connection.close()
        
        print("Health record added successfully.")
    except mysql.connector.Error as error:
        print("Error adding health record:", error)



# Define a handler for processing HTTP requests
class RequestHandler(BaseHTTPRequestHandler):
    # Method to set HTTP headers for the response
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # Handle GET requests
    def do_GET(self):
    
        if self.path == '/':
            # Respond with a welcome message
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Welcome to PHR System"}).encode('utf-8'))
            return

        # Check if the path is for the login endpoint
        if self.path == '/login':
           
            auth_header = self.headers.get('Authorization')

       
            if auth_header and auth_header.startswith('Basic '):
                
                _, encoded_credentials = auth_header.split(' ', 1)
                decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
                username, password = decoded_credentials.split(':', 1)

         
                user_id = basic_authenticate(username, password)
                if user_id:
                 
                    token = generate_token(user_id)
                  
                    self._set_headers()
                    self.wfile.write(json.dumps({"token": token}).encode('utf-8'))
                    return

            # Authorization failed
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))


        if self.path == '/authenticate':
         
            auth_header = self.headers.get('Authorization')

            if auth_header and auth_header.startswith('Bearer '):
                # Extract the token from the authorization header
                _, token = auth_header.split(' ', 1)

                # Authenticate the user using Bearer authentication
                if bearer_authenticate(token):
                    # Authorization successful
                    self._set_headers()
                    self.wfile.write(json.dumps({"message": "Authorization successful"}).encode('utf-8'))
                    return

            # Authorization failed
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))
        
        # Check if the path is for the get_all_health_record endpoint
        if self.path == '/get_all_health_record':
            # Get the authorization header
            auth_header = self.headers.get('Authorization')

            # Check if the request uses Bearer authentication
            if auth_header and auth_header.startswith('Bearer '):
                # Extract the token from the authorization header
                _, token = auth_header.split(' ', 1)

                # Authenticate the user using Bearer authentication
                if bearer_authenticate(token):
                    # Extract user_id from the token
                    try:
                        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                        user_id = payload['user_id']

                        # Connect to the database
                        connection = connect_to_database()
                        cursor = connection.cursor()

                        # Query to fetch all health records for the user
                        query = "SELECT * FROM health_records WHERE patientID = %s"
                        cursor.execute(query, (user_id,))
                        records = cursor.fetchall()

                        # Close cursor and connection
                        cursor.close()
                        connection.close()

                        # Serialize records with date objects converted to ISO format
                        serialized_records = []
                        
                        for record in records:
                            serialized_record = {
                                'patientID': record[1],
                                'date': record[2].isoformat(),  # Convert date to ISO format string
                                'diagnosis': record[3],
                                'treatment': record[4],
                                'medicalcondition': record[5],
                                'familyhistory': record[6],
                                'healthcareprovider': record[7]
                            }
                            serialized_records.append(serialized_record)

                        # Respond with the user's health records
                        self._set_headers()
                        self.wfile.write(json.dumps(serialized_records).encode('utf-8'))
                        return

                    except jwt.ExpiredSignatureError:
                        # Token has expired
                        self._set_headers(401)
                        self.wfile.write(json.dumps({"error": "Token has expired"}).encode('utf-8'))
                        return
                    except jwt.InvalidTokenError:
                        # Invalid token
                        self._set_headers(401)
                        self.wfile.write(json.dumps({"error": "Invalid token"}).encode('utf-8'))
                        return

                else:
                    # Authorization failed
                    self._set_headers(401)
                    self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))
                    return

            else:
                # Authorization header missing
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Authorization header missing"}).encode('utf-8'))
                return


        # Respond with a 404 error for unknown endpoints
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))



  # Handle POST requests
    def do_POST(self):
        # Get the length of the request body
        content_length = int(self.headers['Content-Length'])
        # Read the request body
        post_data = self.rfile.read(content_length)
        # Parse the JSON data
        user_data = json.loads(post_data.decode('utf-8'))
        
        # Debugging: Print the parsed user data
        print("Received User Data:", user_data)

        # Check if the path is for user registration
        if self.path == '/register':
            # Check if all required parameters are provided
            if all(key in user_data for key in ['username', 'password', 'email', 'first_name', 'last_name']):
                # Extract user data
                username = user_data['username']
                password = user_data['password']
                email = user_data['email']
                first_name = user_data['first_name']
                last_name = user_data['last_name']

                # Debugging: Print extracted user data
                print("Username:", username)
                print("Password:", password)
                print("Email:", email)
                print("First Name:", first_name)
                print("Last Name:", last_name)

                # Register the user
                register_user(username, password, email, first_name, last_name)
                # Respond with success message
                self._set_headers()
                self.wfile.write(json.dumps({"message": "User registered successfully"}).encode('utf-8'))
                return
            else:
                # Required parameters are missing, respond with error message
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Missing required parameters"}).encode('utf-8'))
                return

        # Check if the path is for adding health record
        elif self.path == '/add_health_record':
            # Get the authorization header
            auth_header = self.headers.get('Authorization')
            if not auth_header:
                # Authorization header missing, respond with error message
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Authorization header missing"}).encode('utf-8'))
                return
            
            # Check if the request uses Bearer authentication
            if auth_header.startswith('Bearer '):
                # Extract the token from the authorization header
                _, token = auth_header.split(' ', 1)

                # Authenticate the user using Bearer authentication
                if not bearer_authenticate(token):
                    # Unauthorized access, respond with error message
                    self._set_headers(401)
                    self.wfile.write(json.dumps({"error": "Unauthorized access"}).encode('utf-8'))
                    return

                # User authenticated, proceed to add health record
                # Extract health record data
                if all(key in user_data for key in ['date', 'diagnosis', 'treatment']):
                    # Get the user ID from the token
                    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    patient_id = payload['user_id']
                    date = user_data['date']
                    diagnosis = user_data['diagnosis']
                    treatment = user_data['treatment']
                    # Extract additional fields
                    medical_condition = user_data.get('medicalcondition', None)
                    family_history = user_data.get('familyhistory', None)
                    healthcare_provider = user_data.get('healthcareprovider', None)

                    # Add the health record to the database
                    add_health_record(patient_id, date, diagnosis, treatment, medical_condition, family_history, healthcare_provider)

                     # Get the added health record from the database
                    new_record = {
                        'patientID': patient_id,
                        'date': date,
                        'diagnosis': diagnosis,
                        'treatment': treatment,
                        'medicalcondition': medical_condition,
                        'familyhistory': family_history,
                        'healthcareprovider': healthcare_provider
                    }
                    
                    # Respond with success message and the added health record
                    response_data = {
                        "message": "Health record added successfully",
                        "record": new_record
                    }

                    # Respond with success message
                    self._set_headers()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                    #self.wfile.write(json.dumps({"message": "Health record added successfully"}).encode('utf-8'))
                    return
                else:
                    # Required parameters are missing, respond with error message
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Missing required parameters"}).encode('utf-8'))
                    return
            else:
                # Invalid authorization header, respond with error message
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Invalid authorization header"}).encode('utf-8'))
                return



    # Handle PUT requests
    def do_PUT(self):
        # Get the length of the request body
        content_length = int(self.headers['Content-Length'])
        # Read the request body
        put_data = self.rfile.read(content_length)
        # Parse the JSON data
        user_data = json.loads(put_data.decode('utf-8'))
        
        # Debugging: Print the parsed user data
        print("Received User Data:", user_data)

        # Check if the path is for updating user data
        if self.path == '/updateuser':
            # Check if user is authenticated with a valid token
            if 'Authorization' in self.headers:
                auth_header = self.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    _, token = auth_header.split(' ', 1)
                    if bearer_authenticate(token):
                        # Extract user ID from token
                        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                        user_id = payload['user_id']

                        # Update user data
                        if user_data:
                            connection = connect_to_database()
                            cursor = connection.cursor()

                            # Construct the SQL query to update user data
                            query = "UPDATE users SET "
                            query_params = []
                            for key, value in user_data.items():
                                query += f"{key}=%s, "
                                query_params.append(value)
                            query = query.rstrip(', ')  # Remove the trailing comma
                            query += " WHERE user_id=%s"
                            query_params.append(user_id)

                            # Execute the update query
                            cursor.execute(query, tuple(query_params))
                            connection.commit()

                            # Close cursor and connection
                            cursor.close()
                            connection.close()

                            # Respond with success message
                            self._set_headers()
                            self.wfile.write(json.dumps({"message": "User data updated successfully"}).encode('utf-8'))
                            return

            # Authorization failed
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))

    # Handle DELETE requests
    def do_DELETE(self):
        # Check if the path is for deleting user data
        if self.path.startswith('/deleteuserinfo'):
            # Extract the field name from the request path
            field_name = self.path.split('/')[-1]

            # Get the user ID from the token
            if 'Authorization' in self.headers:
                auth_header = self.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    _, token = auth_header.split(' ', 1)
                    if bearer_authenticate(token):
                        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                        user_id = payload['user_id']

                        # Update the specified field value to null/empty
                        connection = connect_to_database()
                        cursor = connection.cursor()

                        query = f"UPDATE users SET {field_name} = NULL WHERE user_id = %s"
                        cursor.execute(query, (user_id,))
                        connection.commit()

                        cursor.close()
                        connection.close()

                        self._set_headers()
                        self.wfile.write(json.dumps({"message": f"{field_name} value deleted successfully"}).encode('utf-8'))
                        return

            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))
        elif self.path == '/deleteuser':
        
            if 'Authorization' in self.headers:
                auth_header = self.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    _, token = auth_header.split(' ', 1)
                    if bearer_authenticate(token):
                        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                        user_id = payload['user_id']

                
                        connection = connect_to_database()
                        cursor = connection.cursor()

                        query = "DELETE FROM users WHERE user_id = %s"
                        cursor.execute(query, (user_id,))
                        connection.commit()

                        cursor.close()
                        connection.close()

                      
                        self._set_headers()
                        self.wfile.write(json.dumps({"message": "User data deleted successfully"}).encode('utf-8'))
                        return

        
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Authorization failed"}).encode('utf-8'))
        else:
           
            self._set_headers(403)
            self.wfile.write(json.dumps({"error": "Forbidden"}).encode('utf-8'))




# start the HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8010):
    server_address = ('', port)
    # start the server class
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")   # Displaying a message indicating server startup
    httpd.serve_forever()  # Starting the server to listen for requests

# Entry point of the script
if __name__ == '__main__':
    # Starting the HTTP server
    run()
