import importlib
import sys

requirements = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "dotenv",
    "sqlalchemy",
    "apscheduler",
    "google.generativeai",
    "googleapiclient",
    "requests"
]

missing = []
for req in requirements:
    try:
        importlib.import_module(req)
    except ImportError:
        # Try mapping common package names to import names
        if req == "dotenv":
            try:
                importlib.import_module("dotenv")
            except ImportError:
                missing.append(req)
        elif req == "google.generativeai":
             try:
                importlib.import_module("google.generativeai")
             except ImportError:
                missing.append("google-genai")
        else:
            missing.append(req)

if missing:
    print(f"Missing dependencies: {', '.join(missing)}")
    sys.exit(1)
else:
    print("All backend dependencies seem to be installed.")
    sys.exit(0)
