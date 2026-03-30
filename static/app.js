/**
 * Frontend JavaScript for Smart Attendance System
 * Author: Ushar Sharma
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Utility function for API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

// Show alert messages
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 5000);
}

// Load students
async function loadStudents() {
    const result = await apiCall('/students');
    if (result.success) {
        updateStudentTable(result.students);
    } else {
        showAlert('Failed to load students: ' + result.error, 'error');
    }
}

// Update student table
function updateStudentTable(students) {
    const tbody = document.querySelector('#studentTable tbody');
    tbody.innerHTML = '';
    
    students.forEach(student => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${student['Roll Number']}</td>
            <td>${student.Name}</td>
        `;
    });
}

// Enroll new student
async function enrollStudent(event) {
    event.preventDefault();
    
    const name = document.getElementById('studentName').value;
    const rollNumber = document.getElementById('rollNumber').value;
    
    if (!name || !rollNumber) {
        showAlert('Please enter both name and roll number', 'error');
        return;
    }
    
    const result = await apiCall('/students', 'POST', {
        name: name,
        roll_number: rollNumber
    });
    
    if (result.success) {
        showAlert('Student enrolled successfully!', 'success');
        document.getElementById('enrollForm').reset();
        loadStudents();
    } else {
        showAlert('Enrollment failed: ' + result.error, 'error');
    }
}

// Load attendance
async function loadAttendance(subject) {
    const result = await apiCall(`/attendance/${subject}`);
    
    if (result.success) {
        updateAttendanceTable(result.records);
    } else {
        showAlert('Failed to load attendance: ' + result.error, 'error');
    }
}

// Update attendance table
function updateAttendanceTable(records) {
    const tbody = document.querySelector('#attendanceTable tbody');
    tbody.innerHTML = '';
    
    records.forEach(record => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${record.Roll_number}</td>
            <td>${record.Name}</td>
            <td>${record.Attendance}</td>
        `;
    });
}

// Load statistics
async function loadStats() {
    const result = await apiCall('/stats');
    
    if (result.success) {
        displayStats(result.stats);
    }
}

// Display statistics
function displayStats(stats) {
    const statsContainer = document.getElementById('statsContainer');
    statsContainer.innerHTML = '';
    
    for (const [subject, data] of Object.entries(stats)) {
        const statCard = document.createElement('div');
        statCard.className = 'stat-card';
        statCard.innerHTML = `
            <div class="stat-value">${data.total_students}</div>
            <div class="stat-label">${subject.toUpperCase()} Students</div>
            <div class="stat-value" style="font-size: 1.5rem; margin-top: 10px;">${data.average_attendance}</div>
            <div class="stat-label">Avg Attendance</div>
        `;
        statsContainer.appendChild(statCard);
    }
}

// Export attendance
async function exportAttendance(subject) {
    window.open(`${API_BASE_URL}/attendance/${subject}/export`, '_blank');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check API health
    apiCall('/health').then(result => {
        if (result.status === 'running') {
            console.log('✅ API Connected');
            loadStudents();
            loadStats();
        } else {
            showAlert('API server not responding', 'error');
        }
    });
});
