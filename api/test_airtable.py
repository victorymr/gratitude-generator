import requests
import json

token = 'pathS7WLkQsG1hLgp.3cf67c637809d11a6629fcfea3102e17b6d9b405b6e612951544a6d94e21568f'
base_id = 'appMbcrkCPHFLf48T'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# First get categories
cat_response = requests.get(
    f'https://api.airtable.com/v0/{base_id}/Categories',
    headers=headers
)

print("Categories Response:")
print(json.dumps(cat_response.json(), indent=2))

# Get a sample of gratitude entries
entries_response = requests.get(
    f'https://api.airtable.com/v0/{base_id}/Gratitude%20Entries',
    headers=headers
)

print("\nGratitude Entries Response:")
print(json.dumps(entries_response.json(), indent=2))
