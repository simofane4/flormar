import os
import shutil

def delete_migrations():
    base_dir = os.getcwd()
    excluded_dirs = {"env", "venv"}  # Add any other directories to exclude

    for root, dirs, files in os.walk(base_dir):
        # Skip excluded directories
        if any(excluded_dir in root for excluded_dir in excluded_dirs):
            continue

        if "migrations" in dirs:
            migrations_dir = os.path.join(root, "migrations")
            for file in os.listdir(migrations_dir):
                if file != "__init__.py":
                    try:
                        os.remove(os.path.join(migrations_dir, file))
                    except PermissionError:
                        print(f"Permission denied: {os.path.join(migrations_dir, file)}")
            
            # Delete the __pycache__ folder if it exists
            pycache_dir = os.path.join(migrations_dir, "__pycache__")
            if os.path.exists(pycache_dir):
                try:
                    shutil.rmtree(pycache_dir)
                except PermissionError:
                    print(f"Permission denied: {pycache_dir}")
            
            print(f"Deleted migrations in: {migrations_dir}")

def main():
    delete_migrations()
    print("Migrations deleted. Now run:")
    print("  python manage.py makemigrations")
    print("  python manage.py migrate")

if __name__ == "__main__":
    main()
