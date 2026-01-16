import os
import zipfile
from pathlib import Path

def create_submission_zip():
    print("Creating submission zip file...")
    print("=" * 50)
    
    # Files to include (in the current directory)
    required_files = [
        'datetime_converter.py',
        'test_convert_date.py', 
        'requirements.txt',
        'setup.py',
        'README.md',
        '__init__.py',
    ]
    
    # Optional files
    optional_files = [
        'edge_cases_test.py',
        'interactive_test.py',
        'example.py',
        'demo_usage.py',
        'run_tests.py',
    ]
    
    # Check which files exist
    existing_files = []
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    # Add optional files if they exist
    for file in optional_files:
        if os.path.exists(file):
            existing_files.append(file)
    
    print(f"Found {len(existing_files)} files:")
    for file in existing_files:
        print(f"  ✓ {file}")
    
    if missing_files:
        print(f"\nMissing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"  ✗ {file}")
    
    # Create zip file
    zip_filename = 'timestamp-converter-project-submission.zip'
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in existing_files:
                zipf.write(file)
                print(f"Added: {file}")
        
        # Get file size
        file_size = os.path.getsize(zip_filename) / 1024  # Convert to KB
        
        print("\n" + "=" * 50)
        print(f"✅ Zip file created successfully!")
        print(f"   File: {zip_filename}")
        print(f"   Size: {file_size:.1f} KB")
        print(f"   Contains: {len(existing_files)} files")
        
        # Show contents of zip
        print("\nContents of zip file:")
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            for name in zipf.namelist():
                print(f"  - {name}")
                
    except Exception as e:
        print(f"\n❌ Error creating zip file: {e}")
    
    print("\n" + "=" * 50)
    print("Your project is ready for submission!")
    print("Submit the file:", zip_filename)

if __name__ == "__main__":
    create_submission_zip()
