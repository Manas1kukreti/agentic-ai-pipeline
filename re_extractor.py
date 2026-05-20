import os
import json

from groq import Groq


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# RE-EXTRACTION FUNCTION
# =========================================================

def re_extract_field(
    email_text,
    failed_field,
    current_value
):

    print(
        f"\nRE-EXTRACTING FIELD: {failed_field}\n"
    )

    prompt = f"""
You are a financial correction engine.

A previous extraction produced an incorrect value.

Your task:
Extract ONLY the correct value for this field
from the email.

STRICT RULES:
1. Return ONLY the corrected value.
2. Do NOT explain anything.
3. Do NOT return JSON.
4. Do NOT generate fake values.
5. If value not found, return EMPTY.

FIELD:
{failed_field}

CURRENT INCORRECT VALUE:
{current_value}

EMAIL:
{email_text}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        corrected_value = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        print(
            f"\nCORRECTED VALUE: "
            f"{corrected_value}\n"
        )

        return corrected_value

    except Exception as e:

        print("\nRE-EXTRACTION FAILED\n")

        print(e)

        return None