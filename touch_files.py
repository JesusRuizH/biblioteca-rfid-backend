from pathlib import Path

files_to_touch = [
    "app/__init__.py",
    "app/main.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/endpoints/__init__.py",
    "app/api/v1/router.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/models/__init__.py",
    "app/models/rfid.py",
    "app/services/__init__.py",
    "app/services/rfid_service.py",
    "app/interfaces/__init__.py",
    "app/interfaces/rfid_handler.py",
    "tests/__init__.py",
    "tests/test_rfid.py",
]

for file in files_to_touch:
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("✅ All files created or touched.")
