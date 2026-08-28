from supabase import create_client, Client
from app.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET,
)

def get_supabase_client() -> Client:
    """
    Initializes and returns a Supabase Client instance.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file_to_supabase(
    file_path: str,
    destination_path: str,
    bucket_name: str = SUPABASE_BUCKET
) -> dict:
    """
    Uploads a local file to Supabase Storage bucket.
    
    :param file_path: Path to the local file to upload.
    :param destination_path: Destination path inside the bucket (e.g., 'SYLLABUS/document.pdf').
    :param bucket_name: Storage bucket name (defaults to SUPABASE_BUCKET).
    :return: Supabase API response dictionary.
    """
    supabase = get_supabase_client()
    with open(file_path, "rb") as f:
        file_content = f.read()

    response = supabase.storage.from_(bucket_name).upload(
        path=destination_path,
        file=file_content,
        file_options={"upsert": "true"}
    )
    return response

def list_bucket_files(
    folder: str = "",
    bucket_name: str = SUPABASE_BUCKET
) -> list:
    """
    Lists files inside a specified folder in the Supabase Storage bucket.
    
    :param folder: Path of the folder inside the bucket (e.g. 'SYLLABUS' or 'SUBJECTS').
    :param bucket_name: Storage bucket name.
    :return: List of file objects inside the folder.
    """
    supabase = get_supabase_client()
    return supabase.storage.from_(bucket_name).list(path=folder)
