This project utilizes a microservices architecture, an innovative architectural style that organizes an application into a series of small, self-contained services, each dedicated to a particular business function. These services operate independently and are interconnected through clearly defined APIs, typically employing lightweight protocols like HTTP/REST for communication. This approach enhances scalability, flexibility, and maintainability, allowing for seamless development, deployment, and management of the system's components.

# Agile Process Documentation

## Vision

**FOR individuals and healthcare providers WHO seek efficient management and access to health records, THE HealthHub is a cloud-based Personal Health Record (PHR) system THAT empowers users with control over their health data, ensuring secure storage, easy accessibility, and seamless sharing. UNLIKE traditional paper-based records or fragmented digital solutions, OUR product provides a centralized platform for comprehensive health management, enabling users to store, manage, and share their health information securely, leading to better informed decisions and improved healthcare outcomes.**

## Product Backlog (User stories)

- As a user, I want to add my medical history to my profile for comprehensive health management.
- As a user, I want to quickly access and view my health record for easy reference.
- As a user, I want to delete irrelevant health records to maintain data privacy and declutter my account.
- As a user, I want to view and edit my personal profile information to ensure accuracy.
- As a user, I want to share selected health records with my healthcare providers securely, ensuring privacy and confidentiality.
- As a user, I want to create an account so that I can securely access my health information.
- As a user, I want to log in to my account using secure authentication methods to protect my data.

## Persona

### John Smith

Meet John Smith, a 45-year-old accountant residing in an urban area with a moderately active lifestyle. As the primary breadwinner for his family of four, John values his health and prioritizes regular check-ups and preventive care. With extensive experience in financial management and accounting practices, John holds a Bachelor's degree in Accounting and Finance and works diligently in a financial firm, handling financial statements, audits, and tax preparations. He seeks a user-friendly tool like the Personal Health Record (PHR) system to manage his health information effectively and efficiently. 

John Smith is interested in the PHR system because it offers him a convenient and efficient way to manage his health information amidst his busy schedule as an accountant. With the PHR, John can easily track his medical history, medications, and appointments, ensuring timely access to relevant healthcare information. The system's user-friendly interface integrates seamlessly into his lifestyle, allowing him to stay organized and informed about his health status while prioritizing privacy and security for the confidentiality of his personal health data.

### Dr. Emily Roberts

Meet Dr. Emily Roberts, a 38-year-old general practitioner residing in a suburban area with her husband and two young children. With over 12 years of experience in providing comprehensive primary care, Dr. Roberts is dedicated to ensuring the well-being of her patients of all ages. Board-certified in family medicine, she holds a Doctor of Medicine (MD) degree and continuously engages in professional development activities to stay abreast of medical advancements. 
Dr. Roberts is keen on using the Personal Health Record (PHR) system to enhance patient care and communication in her practice. With the PHR, she can securely access and manage patients' health records, streamline administrative tasks, and provide personalized care plans, ultimately improving patient outcomes and satisfaction.

### Michael Nguyen

Meet Michael Nguyen, a 40-year-old health administrator residing in a metropolitan area with a passion for improving healthcare delivery. With a Master's degree in Healthcare Administration and extensive experience in healthcare management, Michael oversees the management and coordination of healthcare services within a large hospital network. He is committed to optimizing operational processes, enhancing patient care delivery, and driving innovation within the healthcare organization.

Michael Nguyen sees the PHR system as a valuable tool to streamline data management and improve care coordination within the healthcare organization. With its ability to centralize patient health information and facilitate interoperability, the PHR system aligns with Michael's goal of optimizing healthcare delivery and driving innovation to enhance patient outcomes and satisfaction.


# Security Measures

- **JWT Token Authentication:** Users are authenticated using JSON Web Tokens (JWT) for secure access to the system.
- **Basic Authentication:** Basic authentication is used for login endpoint to authenticate users with username and password.
- **Bearer Authentication:** Bearer authentication is used for other endpoints to authenticate users with JWT token.
- **Password Hashing:** User passwords are hashed using SHA-256 algorithm with a unique salt for enhanced security.


### Containerized Project with Docker Compose

The project is built and run within Docker using Docker Compose. Docker Compose allows for defining and running multi-container Docker applications with a single configuration file (`docker-compose.yml`).

The `docker-compose.yml` file specifies two services: `pythonapp` and `mysql`.

- The `pythonapp` service uses a Dockerfile in the `./systemPHR/` directory to build the Python application image.
- The `mysql` service uses a Dockerfile in the `./mysql/database/` directory to build the MySQL database image and initializes it with a SQL file.

Running `docker-compose up` builds the Docker images and starts the containers. The Python application is accessible at `http://localhost:8010`, interacting with the MySQL database container for data storage.


# API Documentation

## Endpoints

### 1. Login

- **URL:** `/login`
- **Method:** `GET`
- **Description:** Authenticate users with Basic authentication and generate JWT token.
- **Request Header:** 
  - `Authorization`: Basic base64(username:password)
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "token": "generated_jwt_token" }`
  - Failure:
    - Status Code: 401
    - Body: `{ "error": "Authorization failed" }`

### 2. Authenticate

- **URL:** `/authenticate`
- **Method:** `GET`
- **Description:** Authenticate users with Bearer authentication using JWT token.
- **Request Header:** 
  - `Authorization`: Bearer jwt_token
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "Authorization successful" }`
  - Failure:
    - Status Code: 401
    - Body: `{ "error": "Authorization failed" }`

### 3. Register

- **URL:** `/register`
- **Method:** `POST`
- **Description:** Register a new user.
- **Request Body:**
  - `username` (string): User's username
  - `password` (string): User's password
  - `email` (string): User's email address
  - `first_name` (string): User's first name
  - `last_name` (string): User's last name
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "User registered successfully" }`
  - Failure:
    - Status Code: 400
    - Body: `{ "error": "Missing required parameters" }`

### 4. Add Health Record

- **URL:** `/add_health_record`
- **Method:** `POST`
- **Description:** Add a new health record for the authenticated user.
- **Request Header:** 
  - `Authorization`: Bearer jwt_token
- **Request Body:**
  - `date` (string): Date of the health record
  - `diagnosis` (string): Diagnosis information
  - `treatment` (string): Treatment information
  - `medicalcondition` (string, optional): Medical condition details
  - `familyhistory` (string, optional): Family medical history
  - `healthcareprovider` (string, optional): Healthcare provider details
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "Health record added successfully", "record": { ... } }`
  - Failure:
    - Status Code: 400
    - Body: `{ "error": "Missing required parameters" }`
    - Status Code: 401
    - Body: `{ "error": "Unauthorized access" }`

### 5. Update User Data

- **URL:** `/updateuser`
- **Method:** `PUT`
- **Description:** Update user data for the authenticated user.
- **Request Header:** 
  - `Authorization`: Bearer jwt_token
- **Request Body:**
  - User data fields to be updated
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "User data updated successfully" }`
  - Failure:
    - Status Code: 401
    - Body: `{ "error": "Authorization failed" }`

### 6. Delete User Info

- **URL:** `/deleteuserinfo/{field_name}`
- **Method:** `DELETE`
- **Description:** Delete specific user information field.
- **Request Header:** 
  - `Authorization`: Bearer jwt_token
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "{field_name} value deleted successfully" }`
  - Failure:
    - Status Code: 401
    - Body: `{ "error": "Authorization failed" }`

### 7. Delete User

- **URL:** `/deleteuser`
- **Method:** `DELETE`
- **Description:** Delete user account.
- **Request Header:** 
  - `Authorization`: Bearer jwt_token
- **Response:**
  - Success: 
    - Status Code: 200
    - Body: `{ "message": "User data deleted successfully" }`
  - Failure:
    - Status Code: 401
    - Body: `{ "error": "Authorization failed" }`
    - Status Code: 403
    - Body: `{ "error": "Forbidden" }`


