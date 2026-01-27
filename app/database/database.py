from supabase import create_client, Client
from app.core.config import SUPABASE_URL, SUPABASE_KEY

# This class will hold our database connection (as a singleton)
class SupabaseConnection:
    client: Client = None

db_connection = SupabaseConnection()

def connect_to_supabase():
    """
    Connects to Supabase.
    This function should be called once at application startup.
    """
    print("Connecting to Supabase...")
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")
            
        db_connection.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Verify connection (optional simple query)
        # db_connection.client.table("hypotheses").select("count", count="exact").execute()
        
        print(f"Successfully connected to Supabase: {SUPABASE_URL}")
        
    except Exception as e:
        print(f"--- FAILED TO CONNECT TO SUPABASE ---")
        print(f"Error: {e}")
        # We'll let the app exit or fail gracefully at startup
        raise

def get_supabase() -> Client:
    """Helper function to get the supabase client instance."""
    return db_connection.client