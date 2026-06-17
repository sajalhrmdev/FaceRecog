from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import insightface

app = FastAPI()

# face_app = insightface.app.FaceAnalysis()
# face_app.prepare(ctx_id=0)

# face_app = insightface.app.FaceAnalysis(
#     providers=["CPUExecutionProvider"]
# )

# face_app.prepare(ctx_id=-1)

face_app = insightface.app.FaceAnalysis(
    name="buffalo_s",
    providers=["CPUExecutionProvider"]
)
face_app.prepare(ctx_id=-1)
@app.get("/health")
def health():
    return {"success": True}

# @app.post("/embedding")
# async def embedding(file: UploadFile = File(...)):
#     image = Image.open(file.file).convert("RGB")
#     image = np.array(image)

#     faces = face_app.get(image)

#     if len(faces) == 0:
#         return {
#             "success": False,
#             "message": "No face detected"
#         }

#     return {
#         "success": True,
#         "embedding": faces[0].embedding.tolist()
#     }

@app.post("/embedding")
async def embedding(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        image = np.array(image)

        faces = face_app.get(image)

        if not faces:
            return {
                "success": False,
                "message": "No face detected"
            }

        return {
            "success": True,
            "embedding": faces[0].embedding.tolist()
        }

    except Exception:
        return {
            "success": False,
            "message": "Invalid image file"
        }
