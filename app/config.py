import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from the .env file
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Supabase Credentials & Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
SUPABASE_FOLDER = os.getenv("SUPABASE_FOLDER", "raw-documents")
SUPABASE_FOLDER_SUBJECTS = os.getenv("SUPABASE_FOLDER_SUBJECTS", "SUBJECTS")
SUPABASE_FOLDER_SYLLABUS = os.getenv("SUPABASE_FOLDER_SYLLABUS", "SYLLABUS")


# Uploads directory
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

