import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Google API ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# --- Application ---
# We can add more settings here later
IS_DEV_MODE = True