# API Documentation

## Smart Attendance System REST API
**Author:** Ushar Sharma  
**Version:** 2.0.0

## Overview

This REST API provides programmatic access to the Smart Attendance System, enabling integration with web applications, mobile apps, or other services.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. For production use, implement JWT or OAuth2.

## Endpoints

### 1. Health Check
Check if the API server and models are running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "running",
  "timestamp": "2026-03-30T10:30:00",
  "model_loaded": true,
  "mongodb_connected": true
}
```

### 2. Get All Students
Retrieve list of all enrolled students.

**Endpoint:** `GET /api/students`

**Response:**
```json
{
  "success": true,
  "count": 3,
  "students": [
    {"Name": "John Doe", "Roll Number": "1"},
    {"Name": "Jane Smith", "Roll Number": "2"}
  ]
}
```

### 3. Enroll New Student
Add a new student to the system.

**Endpoint:** `POST /api/students`

**Request Body:**
```json
{
  "name": "John Doe",
  "roll_number": "1"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Student enrolled successfully",
  "student": {
    "name": "John Doe",
    "roll_number": "1"
  }
}
```

### 4. Get Attendance Records
Retrieve attendance records for a specific subject.

**Endpoint:** `GET /api/attendance/{subject}`

**Parameters:**
- `subject` (path): Subject name (hindi or english)

**Response:**
```json
{
  "success": true,
  "subject": "hindi",
  "count": 3,
  "records": [
    {"Name": "John Doe", "Roll_number": "1", "Attendance": 5}
  ]
}
```

### 5. Export Attendance
Download attendance records as CSV file.

**Endpoint:** `GET /api/attendance/{subject}/export`

**Parameters:**
- `subject` (path): Subject name (hindi or english)

**Response:** CSV file download

### 6. Get Statistics
Get attendance statistics across all subjects.

**Endpoint:** `GET /api/stats`

**Response:**
```json
{
  "success": true,
  "stats": {
    "hindi": {
      "total_students": 3,
      "total_attendance": 15,
      "average_attendance": 5.0
    },
    "english": {
      "total_students": 3,
      "total_attendance": 12,
      "average_attendance": 4.0
    }
  },
  "timestamp": "2026-03-30T10:30:00"
}
```

### 7. Get Available Subjects
List all available subjects/lectures.

**Endpoint:** `GET /api/subjects`

**Response:**
```json
{
  "success": true,
  "subjects": ["Hindi", "English"]
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (MongoDB not connected)

## Usage Examples

### Python
```python
import requests

# Get all students
response = requests.get('http://localhost:5000/api/students')
students = response.json()

# Enroll new student
data = {"name": "John Doe", "roll_number": "1"}
response = requests.post('http://localhost:5000/api/students', json=data)
```

### JavaScript
```javascript
// Get attendance
fetch('http://localhost:5000/api/attendance/hindi')
  .then(res => res.json())
  .then(data => console.log(data));

// Enroll student
fetch('http://localhost:5000/api/students', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'John Doe', roll_number: '1' })
});
```

### cURL
```bash
# Health check
curl http://localhost:5000/api/health

# Get students
curl http://localhost:5000/api/students

# Enroll student
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","roll_number":"1"}'

# Get attendance
curl http://localhost:5000/api/attendance/hindi

# Export attendance
curl http://localhost:5000/api/attendance/hindi/export -o attendance.csv
```

## Future Enhancements

- JWT authentication
- WebSocket support for real-time updates
- Image upload endpoint for remote face recognition
- Batch operations
- Advanced filtering and search
- Rate limiting
- API versioning
