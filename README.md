# Gratitude Generator

A web application and API that generates random gratitude messages based on different life categories.

## Features

- Select from multiple categories (home, family, friends, money, nature, spouse, health)
- Get random gratitude messages for each category
- Clean and responsive user interface
- RESTful API for programmatic access
- Airtable backend for easy content management

## Web Application Usage

Simply open `index.html` in a web browser to use the application. Select a category from the dropdown menu and click "Get Gratitude Message" to receive a random gratitude message.

## API Usage

The application provides a RESTful API built with FastAPI. Here are the available endpoints:

### List Categories
```bash
GET /categories
```
Returns a list of available gratitude categories.

### Get Gratitude Messages
```bash
GET /gratitude?categories=family&count=2
```
Parameters:
- `categories`: One or more category names (required)
- `count`: Number of messages to return (default: 1, max: 5)

### Add New Gratitude Message
```bash
POST /gratitude
Content-Type: application/json

{
    "category": "family",
    "statement": "I am grateful for family dinners"
}
```

## Technical Stack

### Web Application
- Vanilla HTML, CSS, and JavaScript
- Airtable API for data storage
- Responsive design for desktop and mobile

### API
- FastAPI framework
- Python 3.12+
- Airtable as backend database
- Uvicorn ASGI server

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gratitude-generator.git
cd gratitude-generator
```

2. Install API dependencies:
```bash
cd api
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the `api` directory with:
```
AIRTABLE_TOKEN=your_token_here
AIRTABLE_BASE_ID=your_base_id_here
```

4. Start the API server:
```bash
uvicorn main:app --reload
```

5. Open `index.html` in your web browser to use the web application.

## API Documentation

Once the API server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## Contributing

Feel free to submit issues and enhancement requests!
