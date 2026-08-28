import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET,
    SUPABASE_FOLDER_SYLLABUS,
    SUPABASE_FOLDER_SUBJECTS,
)
from app.supabase_client import (
    get_supabase_client,
    upload_file_to_supabase,
    list_bucket_files,
)

def upload_from_source_dir(source_dir_path: str):
    source_path = Path(source_dir_path).resolve()
    if not source_path.exists():
        print(f"[FAIL] Source directory does not exist: {source_path}")
        return

    print(f"\n[SCAN] Scanning source directory: {source_path}")
    
    # Recursively find all PDF and document files
    files_to_upload = list(source_path.rglob("*.*"))
    # Filter out directories
    files_to_upload = [f for f in files_to_upload if f.is_file() and not f.name.startswith(".")]

    if not files_to_upload:
        print("[WARN] No files found in the specified source directory.")
        return

    print(f"Found {len(files_to_upload)} file(s) to upload:\n")

    for file_p in files_to_upload:
        # Determine target folder (SYLLABUS or SUBJECTS based on relative path or file name)
        rel_path = file_p.relative_to(source_path)
        
        # Check if relative path contains folder indicators
        parts = rel_path.parts
        if len(parts) > 1 and parts[0].upper() in [SUPABASE_FOLDER_SYLLABUS.upper(), SUPABASE_FOLDER_SUBJECTS.upper()]:
            remote_path = "/".join(parts)
        else:
            # Default to SUBJECTS if not explicitly under SYLLABUS
            target_folder = SUPABASE_FOLDER_SYLLABUS if "syllabus" in file_p.name.lower() else SUPABASE_FOLDER_SUBJECTS
            remote_path = f"{target_folder}/{file_p.name}"

        print(f"Uploading '{rel_path}' -> Supabase bucket '{SUPABASE_BUCKET}/{remote_path}'...")
        try:
            res = upload_file_to_supabase(str(file_p), remote_path)
            print(f" [OK] Success: {res}")
        except Exception as e:
            print(f" [FAIL] Error uploading {file_p.name}: {e}")

def main():
    print("=== NEXORA Supabase Storage Batch Uploader ===")
    print(f"Supabase URL:  {SUPABASE_URL}")
    print(f"Target Bucket: {SUPABASE_BUCKET}\n")

    # 1. Test Supabase Client Connection
    try:
        supabase = get_supabase_client()
        print("[OK] Supabase Client connected successfully.")
    except Exception as e:
        print(f"[FAIL] Failed to initialize Supabase client: {e}")
        return

    # 2. Check source directory argument or prompt user
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
        upload_from_source_dir(source_dir)
    else:
        print("\n[INFO] No source directory passed as CLI argument.")
        print("Usage:")
        print("  python upload_test.py \"C:\\Path\\To\\Your\\Source\\Folder\"")
        print("\nOr place PDF files in the 'uploads/' folder and pass its path.")

if __name__ == "__main__":
    main()
