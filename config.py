import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# Gemini
# ===========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)

# ===========================
# Server
# ===========================

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", "8000"))