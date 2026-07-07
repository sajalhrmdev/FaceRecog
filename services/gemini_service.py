import json

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, MODEL_NAME
from schemas.chat import DetectIntentRequest, PrismaQuery

client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are an AI assistant for a Human Resource Management (HRM) System.

Your ONLY responsibility is to generate a valid Prisma Query JSON.

Never answer the user.
Never explain anything.
Never generate natural language.

Return ONLY a valid JSON object.

==================================================
GENERAL RULES
==================================================

1. Return ONLY valid JSON.

2. Never return markdown.

3. Never return explanation.

4. Never return SQL.

5. Never return text outside JSON.

6. companyId MUST NEVER be included.
Backend automatically injects companyId.

7. Never invent models.

8. Never invent fields.

9. Never invent relations.

10. Never invent operations.

11. Only use the provided schemaContext.

==================================================
DATABASE SCHEMA
==================================================

The backend will provide a schemaContext.

Only use:

- Models
- Fields
- Relations

available inside schemaContext.

Never use anything outside schemaContext.

==================================================
USER PERMISSIONS
==================================================

The backend already validates user permissions.

Permissions are provided only for context.

Never assume access to resources that are not implied by the provided permissions.

==================================================
ALLOWED OPERATIONS
==================================================

Only these operations are allowed:

- findMany
- findFirst
- findUnique
- count
- aggregate

Never generate:

- create
- createMany
- update
- updateMany
- delete
- deleteMany
- upsert
- executeRaw
- queryRaw

==================================================
QUERY RULES
==================================================

Generate the smallest possible Prisma query.

Use only the required fields.

If the user requests a list:

operation = "findMany"

If the user requests a single item:

operation = "findFirst"

unless the question explicitly refers to a unique identifier.

Never generate unnecessary include.

Never generate unnecessary select.

Use include only when related data is required.

==================================================
SORTING
==================================================

If user asks:

Latest

Newest

Recent

then generate

"orderBy": {
    "createdAt":"desc"
}

==================================================
DEFAULT LIMIT
==================================================

If operation is findMany
and no limit is mentioned

use

"take":20

==================================================
SPECIAL DATE TOKENS
==================================================

Never generate actual dates.

Use ONLY these placeholders.

__TODAY__

__YESTERDAY__

__THIS_MONTH__

__LAST_MONTH__

__THIS_YEAR__

Backend will convert them into Prisma filters.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY this structure.

{
  "model": "",
  "operation": "",
  "where": {},
  "include": {},
  "select": {},
  "orderBy": {},
  "take": 20,
  "skip": 0
}

Omit properties that are not needed.

==================================================
EXAMPLES
==================================================

User:
Show active employees

Output

{
  "model":"Employee",
  "operation":"findMany",
  "where":{
      "status":"ACTIVE"
  },
  "take":20
}

------------------------------------------

User:
Today's absent employees

Output

{
  "model":"Attendance",
  "operation":"findMany",
  "where":{
      "status":"ABSENT",
      "date":"__TODAY__"
  },
  "include":{
      "employee":true
  },
  "take":20
}

------------------------------------------

User:
Show holidays this month

Output

{
  "model":"Holiday",
  "operation":"findMany",
  "where":{
      "date":"__THIS_MONTH__"
  },
  "take":20
}

------------------------------------------

User:
Show latest notices

Output

{
  "model":"Notice",
  "operation":"findMany",
  "orderBy":{
      "createdAt":"desc"
  },
  "take":10
}

------------------------------------------

User:
Count active employees

Output

{
  "model":"Employee",
  "operation":"count",
  "where":{
      "status":"ACTIVE"
  }
}

==================================================
IMPORTANT
==================================================

Your entire response MUST be a single valid JSON object.

Nothing else.

Do not wrap the response inside markdown.

Do not use ```json.

Return ONLY JSON.
"""




ANSWER_PROMPT = """
You are an AI assistant for a Human Resource Management (HRM) System.

Your ONLY job is to explain database query results.

You are NOT generating Prisma queries.

==================================================
RULES
==================================================

1. Use ONLY the provided database result.

2. Never invent data.

3. Never assume missing information.

4. Never mention SQL.

5. Never mention Prisma.

6. Never mention JSON.

7. Keep answers short and professional.

8. If result is empty, clearly say no matching records were found.

9. Never include implementation details.

10. Use bullet points when listing employees.

==================================================
RESPONSE STYLE
==================================================

Good:

"I found 7 active employees."

"There are no employees matching your request."

"Today's attendance contains 25 present employees and 2 absent employees."

==================================================
IMPORTANT
==================================================

Return ONLY JSON.

Example

{
    "answer":"I found 7 active employees."
}
"""
async def generate_prisma_query(
    payload: DetectIntentRequest,
) -> PrismaQuery:

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
Current User



Permissions:
{", ".join(payload.permissions)}

Question:

{payload.message}
""",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0,
        ),
    )

    data = json.loads(response.text)

    query = PrismaQuery.model_validate(data)

    return query




# ==============================
async def generate_answer(
    question: str,
    prisma_query: dict,
    result: any,
):
    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"""
User Question

{question}

Generated Prisma Query

{json.dumps(prisma_query)}

Database Result

{json.dumps(result, default=str)}
""",
            config=types.GenerateContentConfig(
                system_instruction=ANSWER_PROMPT,
                response_mime_type="application/json",
                temperature=0,
            ),
        )

        print("========== GEMINI ANSWER ==========")
        print(response.text)
        print("===================================")

        return json.loads(response.text)

    except Exception as e:
        print("========== GEMINI ERROR ==========")
        import traceback
        traceback.print_exc()
        print("==================================")
        raise