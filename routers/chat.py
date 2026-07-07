from fastapi import APIRouter

from schemas.chat import (
    DetectIntentRequest,
    GenerateAnswerRequest,
)

from services.gemini_service import (
    generate_prisma_query,
    generate_answer,
)

router = APIRouter()


# ======================================================
# Generate Prisma Query
# ======================================================

@router.post("/intent")
async def generate_query(
    payload: DetectIntentRequest,
):
    try:

        result = await generate_prisma_query(payload)

        return {
            "success": True,
            "data": result.model_dump(),
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e),
        }


# ======================================================
# Generate Human Answer
# ======================================================

@router.post("/answer")
async def generate_ai_answer(
    payload: GenerateAnswerRequest,
):
    try:

        result = await generate_answer(
            question=payload.question,
            prisma_query=payload.prismaQuery.model_dump(),
            result=payload.result,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e),
        }