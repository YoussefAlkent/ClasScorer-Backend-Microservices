# Classroom Monitoring System

This is a microservices-based application designed to monitor classrooms and track students' participation in real-time. The system is capable of detecting various student activities such as gaze estimation and hand-raising, and records their attendance, focus, and engagement during lectures.

## Features

- **Real-time Gaze Estimation**: Detects whether a student is looking at the screen during a lecture.
- **Hand-Raising Detection**: Detects when a student raises their hand.
- **Student Localization**: Identifies the location of students in a classroom environment.
- **Storage Proxy**: Manages course, student, and tutor data, including registration and login functionality.
- **Prometheus & Grafana Monitoring**: Monitors all services and visualizes metrics in real-time.

## Architecture

The system is designed using microservices that communicate through Kafka. Each service is isolated in its own container, allowing for better scalability and maintainability. The architecture consists of the following services:

### 1. **Person Localization**
- Detects and localizes students in the classroom.
- Communicates with Kafka to forward detected students' data.

### 2. **Gaze Detection**
- Performs gaze estimation to check whether a student is focused on the lecture.
- Receives image data from Kafka and sends the gaze estimation results.

### 3. **Hand Raising Detection**
- Detects when a student raises their hand.
- Receives student data from Kafka and sends the hand-raising detection results.

### 4. **Student Detection**
- Analyzes the student's participation (e.g., focus percentage, hand raising) and attendance.
- Tracks the student's interactions and sends data to the storage proxy for recording.

### 5. **Storage Proxy**
- Manages user accounts, courses, student records, and attendance data.
- Handles account creation and login for tutors and students.
- Stores course and lecture data along with student participation statistics (focus percentage, hand-raising count, attendance).

### 6. **Prometheus**
- Monitors all services and stores metrics in a time-series database.

### 7. **Grafana**
- Visualizes data collected by Prometheus.
- Provides a dashboard for real-time monitoring of all services.

## Services Communication

- Kafka is used for communication between the services. Each service listens to relevant Kafka topics and processes the data.
- Data is stored in a PostgreSQL database by the **Storage Proxy** service, which handles all data storage operations.

## Technology Stack

- **Backend**: FastAPI (for REST APIs)
- **Machine Learning**: PyTorch, TensorFlow
- **Kafka**: For message-based communication
- **Database**: PostgreSQL (for storing user and course data)
- **Monitoring**: Prometheus (metrics collection), Grafana (dashboard and visualization)
- **Containerization**: Docker and Docker Compose

## Getting Started

### Prerequisites

1. **Docker** and **Docker Compose** installed on your machine.
2. **PostgreSQL** installed or running in a Docker container.
3. **Kafka** and **Zookeeper** running in Docker containers.

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/YoussefAlkent/ClasScorer-Backend-Microservices
   cd ClasScorer-Backend-Microservices
	```
2. Build and start the containers:
	```bash
	docker-compose up --build
	```
This command will start all the services, including:
-  Kafka and Zookeeper
- Person Localization Service
- Gaze Detection Service
- Hand-Raising Detection Service
- Student Detection Service
- Storage Proxy Service
- Prometheus (for monitoring)
- Grafana (for visualization)

3. Access the services:
- FastAPI endpoints (for each service) will be accessible on the ports configured in the docker-compose.yml file (e.g., http://localhost:8000 for the Storage Proxy service).
- Grafana will be available at http://localhost:3000 (default credentials: admin/admin).
- Prometheus will be available at http://localhost:9090.

4. For monitoring:
- You can view real-time metrics in Grafana using the Prometheus data source.

### Kafka Topics

The following Kafka topics are used for communication between the services:

- gaze_input: Sent by the Person Localization service, containing student images and bounding box data for gaze estimation.
- gaze_output: Contains gaze estimation results, sent by the Gaze Detection service.
- hand_raising_input: Sent by the Person Localization service, containing student images for hand-raising detection.
- hand_raising_output: Contains hand-raising detection results, sent by the Hand Raising Detection service.
- student_activity: Contains processed student activity (focus, hand-raising count, attendance), sent by the Student Detection service to the Storage Proxy.

## Database Schema

The system uses a PostgreSQL database with the following tables:

- Users: Stores user account information (e.g., username, email, password, etc.).
- Courses: Stores course details.
- Lectures: Stores lecture-specific data and links it to courses.
- Students: Stores student information, including the facial recognition vector (in BYTEA format).
- StudentActivity: Tracks student participation metrics per lecture (e.g., focus percentage, hand-raising count).
- StudentCourseLink: Links students to courses and lectures they attend.

## Future Work

- User Authentication: Implement OAuth and JWT authentication for better security and user management.
- Enhanced Analytics: Provide more in-depth analytics and reports for tutors to track student performance and participation trends.

## License

MIT License - see the LICENSE file for details.
