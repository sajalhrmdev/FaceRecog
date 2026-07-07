from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ======================================================
# Detect Intent Request
# ======================================================

class DetectIntentRequest(BaseModel):
    companyId: int

    userId: int

    permissions: List[str]

    schemaContext: str

    message: str


# ======================================================
# Prisma Query
# ======================================================

class PrismaQuery(BaseModel):

    model: str

    operation: str

    where: Optional[Dict[str, Any]] = None

    include: Optional[Dict[str, Any]] = None

    select: Optional[Dict[str, Any]] = None

    orderBy: Optional[Dict[str, Any]] = None

    take: Optional[int] = Field(default=20)

    skip: Optional[int] = Field(default=0)


# ======================================================
# Generate Answer Request
# ======================================================

class GenerateAnswerRequest(BaseModel):

    question: str

    prismaQuery: PrismaQuery

    result: Any


# ======================================================
# Generate Answer Response
# ======================================================

class GenerateAnswerResponse(BaseModel):

    answer: str