import json
import os
from supabase import create_client

# Your Supabase Credentials
URL = "https://skycmsmjgfqsphasilba.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNreWNtc21qZ2Zxc3BoYXNpbGJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyMjU0ODksImV4cCI6MjA4NTgwMTQ4OX0.zks6TXbA3LLYuOBuNSnj2UU46stlpfnz4BZd3u1U95o"

supabase = create_client(URL, KEY)

def migrate_table(filename, table_name, transform_func):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            # Transform dictionary format to list of rows for SQL
            rows = transform_func(data)
            if rows:
                print(f"Uploading {len(rows)} rows to {table_name}...")
                supabase.table(table_name).upsert(rows).execute()
                print(f"Successfully migrated {table_name}!")
    else:
        print(f"File {filename} not found. Skipping.")

# --- Transformation Logic ---

def transform_users(data):
    return [{"uid": k, "pwd": v['pwd'], "role": v['role'], "name": v['name']} for k, v in data.items()]

def transform_docs(data):
    return [{
        "name": k, 
        "spec": v['spec'], 
        "status": v['status'], 
        "room": v['room'], 
        "tokens": v['tokens'],
        "last_token_num": v.get('last_token_num', 0),
        "last_date": v.get('last_date', "")
    } for k, v in data.items()]

def transform_inv(data):
    return [{"item": k, "quantity": v} for k, v in data.items()]

def transform_beds(data):
    return [{"bed_id": k, "status": v} for k, v in data.items()]

def transform_hist(data):
    # Mapping old TitleCase JSON keys to lowercase SQL columns
    return [{
        "date": r["Date"], "time": r["Time"], "patient": r["Patient"],
        "doctor": r["Doctor"], "token": r["Token"], "specialty": r["Specialty"]
    } for r in data]

# --- Run Migration ---
if __name__ == "__main__":
    migrate_table('ns_users.json', 'users', transform_users)
    migrate_table('ns_doctors.json', 'doctors', transform_docs)
    migrate_table('ns_inventory.json', 'inventory', transform_inv)
    migrate_table('ns_beds.json', 'beds', transform_beds)
    migrate_table('ns_history.json', 'history', transform_hist)
    print("\nMigration Complete. You can now delete your JSON files.")