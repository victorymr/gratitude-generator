from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Airtable configuration
AIRTABLE_TOKEN = "pathS7WLkQsG1hLgp.3cf67c637809d11a6629fcfea3102e17b6d9b405b6e612951544a6d94e21568f"
AIRTABLE_BASE_ID = "appMbcrkCPHFLf48T"
AIRTABLE_API_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

class GratitudeEntry(BaseModel):
    category: str
    statement: str

@app.get("/categories", response_model=List[str])
async def get_categories():
    """Get all available gratitude categories"""
    try:
        response = requests.get(
            f"{AIRTABLE_API_URL}/Categories",
            headers=headers
        )
        response.raise_for_status()
        categories = [record['fields']['Category Name'] 
                     for record in response.json()['records']
                     if 'Category Name' in record['fields']]
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gratitude")
async def get_gratitude(
    categories: List[str] = Query(None),
    count: int = Query(default=1, ge=1, le=5)
):
    """Get random gratitude messages for specified categories"""
    try:
        if not categories:
            raise HTTPException(status_code=400, detail="At least one category is required")

        print(f"Fetching gratitude messages for categories: {categories}")

        # Get entries from Airtable based on category name
        response = requests.get(
            f"{AIRTABLE_API_URL}/Gratitude%20Entries",
            headers=headers
        )
        response.raise_for_status()
        entries_data = response.json()
        print(f"Entries response: {entries_data}")
        
        # Extract gratitude statements
        entries = []
        for record in entries_data.get('records', []):
            if 'Gratitude Statement' in record['fields']:
                entries.append({
                    "category": categories[0],
                    "statement": record['fields']['Gratitude Statement']
                })

        if not entries:
            raise HTTPException(
                status_code=404,
                detail="No gratitude messages found for the specified categories"
            )

        # Return random entries up to the requested count
        return random.sample(entries, min(count, len(entries)))

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gratitude")
async def create_gratitude(entry: GratitudeEntry):
    """Create a new gratitude entry"""
    try:
        # First, get or create the category
        cat_response = requests.get(
            f"{AIRTABLE_API_URL}/Categories",
            headers=headers,
            params={
                "filterByFormula": f"{{Category Name}}='{entry.category}'"
            }
        )
        cat_response.raise_for_status()
        
        cat_data = cat_response.json()
        if not cat_data['records']:
            # Create new category
            cat_create_response = requests.post(
                f"{AIRTABLE_API_URL}/Categories",
                headers=headers,
                json={
                    "records": [{
                        "fields": {
                            "Category Name": entry.category
                        }
                    }]
                }
            )
            cat_create_response.raise_for_status()
            category_id = cat_create_response.json()['records'][0]['id']
        else:
            category_id = cat_data['records'][0]['id']

        # Create the gratitude entry
        response = requests.post(
            f"{AIRTABLE_API_URL}/Gratitude%20Entries",
            headers=headers,
            json={
                "records": [{
                    "fields": {
                        "Category": [category_id],
                        "Gratitude Statement": entry.statement
                    }
                }]
            }
        )
        response.raise_for_status()
        
        return {"message": "Gratitude entry created successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
