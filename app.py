
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import insightface
from routers.chat import router as chat_router

app = FastAPI()

# Default model = buffalo_l
face_app = insightface.app.FaceAnalysis(
    providers=["CPUExecutionProvider"]
)

face_app.prepare(ctx_id=-1)


@app.get("/health")
def health():
    return {"success": True}


@app.post("/embedding")
async def embedding(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        image = np.array(image)

        faces = face_app.get(image)

        if len(faces) == 0:
            return {
                "success": False,
                "message": "No face detected"
            }

        return {
            "success": True,
            "embedding": faces[0].embedding.tolist()
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    

    # ===================================
  

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["AI Chat"]
)