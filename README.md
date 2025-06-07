# 📘Fitness Class Booking

> A Django REST API for a fitness booking system that allows users to view classes, book slots, and manage their accounts

## 🚀 Features

- User registration & authentication (JWT)
- Class listings & bookings
- Swagger API documentation
- ✅ Pre-commit hooks, Linting, and Code Formatting

## 📦 Apps Overview

- **core** – Contains shared components like custom decorators (token_required), utility functions (e.g.send_email), and base models used across other apps.
- **authentication** – Handles user registration, login, and authentication (e.g., JWT).
- **booking** –Handles fitness class listings, slot bookings, and booking-related data management.

## 🛠️ Tech Stack

- **Python** 3.x
- **Django** & **Django REST Framework**
- **PostgreSQL**
- **drf-yasg** (for Swagger)
- **black** (for code formatting)
- **flake8** (for linting and code style enforcement)
- **pre-commit** (to automate linting/formatting before commits)
- **pylint** (for additional static code analysis)

## ⚙️ Setup Instructions

# 1. Clone the repository

git clone https://github.com/Poooooooooja-k/Booking.git
cd booking

# 2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# 3. Install dependencies

pip install -r requirements.txt

# 4. Run migrations

python manage.py migrate

# 5. Start the server

python manage.py runserver

# 6. Seed sample data

python manage.py loaddata seed/initial_data.json

# Swagger UI: http://localhost:8000/swagger/

## 🔐 Authentication API - Sample Requests

# 1. User signup

curl -X POST http://localhost:8000/auth/v1/signup/ \
 -H "Content-Type: application/json" \
 -d '{
"name": "Pooja K",
"email": "pooja@example.com",
"password": "strongpassword123",
"age": 25,
"phone_number": "9876543210"
}'

# 2. User login

curl -X POST http://localhost:8000/auth/v1/login/ \
 -H "Content-Type: application/json" \
 -d '{
"email": "pooja@example.com",
"password": "strongpassword123"
}'

# 3 . Update User

curl -X PUT http://localhost:8000/auth/v1/update_user/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <your_token_here>" \
 -d '{
"email": "pooja@example.com",
"name": "Pooja Kumar",
"age": 26
}'

# 4. Get all users

curl -X GET http://localhost:8000/auth/v1/user_list/ \
 -H "Authorization: Bearer <your_token_here>"

# 5 . Get User By Id

curl -X GET "http://localhost:8000/auth/v1/user_list_by_id/?id=1" \
 -H "Authorization: Bearer <your_token_here>"

# 6. Delete user (soft delete)

curl -X DELETE http://localhost:8000/auth/v1/delete_user/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <your_token_here>" \
 -d '{"id": 1}'

## 🔐 Booking API - Sample Requests

# 1. Create class type

curl -X POST http://localhost:8000/bookings/v1/create_class_type/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <your_token_here>" \
 -d '{
"name": "Yoga",
"description": "Beginner level yoga session"
}'

# 2. List all class types

curl -X GET http://localhost:8000/bookings/v1/list_class/ \
 -H "Authorization: Bearer <your_token_here>"

# 3.Retrieve Class Type by ID

curl -X GET "http://localhost:8000/bookings/v1/retrive_class/?id=1" \
 -H "Authorization: Bearer <your_token_here>"

# 4.Update Class Type

curl -X PUT http://localhost:8000/bookings/v1/Update_class_type/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <your_token_here>" \
 -d '{
"id": 1,
"name": "Advanced Yoga",
"description": "For experienced participants"
}'

# 5.Soft delete class type

curl -X DELETE http://localhost:8000/bookings/v1/delete_class_type/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <your_token_here>" \
 -d '{"id": 1}'

# 6 .Create fitness class
curl -X POST http://localhost:8000/bookings/v1/create_fitness_class/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token_here>" \
  -d '{
    "class_type": 1,
    "instructor_name": "Anjali Mehta",
    "start_time": "2025-06-10T07:00:00Z",
    "end_time": "2025-06-10T08:00:00Z",
    "capacity": 20
}'


# 7. List all fitness class
curl -X GET http://localhost:8000/bookings/v1/list_fitness_class/ \
  -H "Authorization: Bearer <your_token_here>"

# 8.Retrieve Fitness Class by ID
curl -X GET "http://localhost:8000/bookings/v1/retrieve_fitness_class/?id=1" \
  -H "Authorization: Bearer <your_token_here>"


# 9. Update Fitness Class
curl -X PUT http://localhost:8000/bookings/v1/update_fitness_class/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token_here>" \
  -d '{
    "id": 1,
    "instructor_name": "Anjali M.",
    "capacity": 25
}'

# 10. soft delete
curl -X DELETE http://localhost:8000/bookings/v1/delete_fitness_class/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token_here>" \
  -d '{"id": 1}'

# 11. book a class slot
curl -X POST http://localhost:8000/bookings/v1/book_slot/ \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
}'

# 12. cancel a booking
curl -X POST "http://localhost:8000/bookings/v1/cancel_booking/?booking_id=1" \
  -H "Authorization: Bearer <your_token_here>"

# 13. List All Bookings by User Email
curl -X GET "http://localhost:8000/bookings/v1/user_bookings/" \
  -H "Authorization: Bearer <your_token_here>"

# 14. List Upcoming Classes
curl -X GET http://localhost:8000/bookings/v1/list_upcoming_class/


