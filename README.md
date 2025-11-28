Event API
Overview

The Event API allows authenticated users to view and filter events by category, title, or description. Users can search for specific events and explore categories efficiently.

Features

Authenticated access only

View all events

Filter events by category

Search events by title or description

Works with Django REST Framework (DRF) and supports Swagger documentation

Requirements

Python 3.10+

Django 4.x

Django REST Framework

drf-spectacular (for Swagger/OpenAPI support)

Virtual environment (recommended)

Installation

Clone the repository:

git clone <your-repo-url>
cd <your-repo-folder>


Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser (optional, for admin panel):

python manage.py createsuperuser


Run the development server:

python manage.py runserver

API Endpoints
Get all events
GET /api/events/


Authentication required

Returns a list of all events

Filter events by category
GET /api/events/?category=<category_id>


Replace <category_id> with the ID of the desired category

Search events by title or description
GET /api/events/?search=<keyword>


Replace <keyword> with the search term

Combine category filter and search
GET /api/events/?category=<category_id>&search=<keyword>

Authentication

The API requires token or session authentication

Only authenticated users can access the events endpoint

Swagger Documentation

Accessible at:

/swagger/  # if using drf-spectacular default setup


Allows testing query parameters (category and search) directly in the browser

Example Request
GET /api/events/?category=1&search=concert
Authorization: Token <your_token>


Response:

[
    {
        "id": 5,
        "organizer": 2,
        "category": 1,
        "title": "Music Concert",
        "description": "An evening of classical music.",
        "date": "2025-12-05T18:00:00Z",
        "location": "City Hall",
        "created_at": "2025-11-28T10:00:00Z"
    }
]

License

This project is licensed under the MIT License.
