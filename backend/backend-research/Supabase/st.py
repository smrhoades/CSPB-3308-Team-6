"""
Purpose: Testing out Supabase API
Author:  Daniel Williams
Usage:   python st.py

Supabase Python API reference: 
https://supabase.com/docs/reference/python/introduction

Also: 
Need to create a .env file that looks like .env.example, AND add .env to 
your .gitignore so we don't expose any secret keys.

The Supabase URL and Key are in the Project Settings panel on the project 
dashboard (lower left corner).
"""

import os
import supabase
from dotenv import load_dotenv
from datetime import datetime, timezone
from supabase import create_client, Client
from werkzeug.security import generate_password_hash

# Load environ variables from .env
load_dotenv()

url: str = os.environ['SUPABASE_URL']
key: str = os.environ['SUPABASE_KEY']
supabase: Client = create_client(url, key)

username1 = 'test'
password1 = generate_password_hash('test')

# .isoformat() to make datetime object JSON-compatible
now_utc = datetime.now(timezone.utc).isoformat()


# Insert test username/password into data (will produce error since entry already exists)
# can uncomment the second command to delete the entry then run this one again
response = (
    supabase.table("user_data")
    .insert({"id": 1, "user_name": username1, 
             "user_pwd": password1, 
             "created_at": now_utc, 
             "modified_at": now_utc})
    .execute()
)

# response = (
#     supabase.table("user_data")
#     .delete()
#     .eq("id", 1)
#     .execute()
# )

print(response)
