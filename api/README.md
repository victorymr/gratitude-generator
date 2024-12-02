# Gratitude Generator API

A FastAPI-based REST API for generating and managing gratitude messages across different life categories.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Airtable API token to the `.env` file

3. Run the API:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### GET /categories
Get all available gratitude categories.

### GET /gratitude
Get random gratitude messages for specified categories.

Query Parameters:
- `categories`: List of category names (required)
- `count`: Number of messages to return (default: 1, max: 5)

Example:
```
GET /gratitude?categories=Family&categories=Work&count=2
```

### POST /gratitude
Create a new gratitude entry.

Request Body:
```json
{
    "category": "Family",
    "statement": "I am grateful for my supportive family"
}
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation at http://localhost:8000/docs
- Alternative documentation at http://localhost:8000/redoc
