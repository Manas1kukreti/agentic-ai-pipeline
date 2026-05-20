import os
from groq import Groq


# =========================================================
# CREATE GROQ CLIENT
# =========================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# MAIN EXTRACTION FUNCTION
# =========================================================

def extract_data(email_text):

    print("\n🧠 SENDING DATA TO GROQ...\n")

    # =====================================================
    # STRICT EXTRACTION PROMPT
    # =====================================================

    prompt = f"""
You are an expert financial data extraction system.

Your task is to extract ONLY the financial transaction
information explicitly present in the email.

STRICT RULES:

1. ONLY extract information present in the email.
2. DO NOT generate fake transactions.
3. DO NOT hallucinate values.
4. DO NOT create random names or amounts.
5. DO NOT assume missing values.
6. If any value is missing, return empty string "".
7. Return ONLY valid JSON.
8. Return ONLY JSON array.
9. DO NOT add markdown.
10. DO NOT add explanations.
11. DO NOT add comments.
12. DO NOT generate sample data.
13. Extract MAXIMUM 10 transactions only.
14. Stop immediately after the final JSON bracket ].

Required JSON format:

[
    {{
        "customer_name": "",
        "account_number": "",
        "transaction_id": "",
        "transaction_date": "",
        "amount": "",
        "currency": "",
        "transaction_type": "",
        "merchant_name": "",
        "invoice_id": "",
        "payment_method": "",
        "status": ""
    }}
]

EMAIL CONTENT:
{email_text}
"""

    try:

        # =================================================
        # GROQ API CALL
        # =================================================

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict JSON financial "
                        "extraction engine."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            max_tokens=4000
        )

        # =================================================
        # EXTRACT OUTPUT
        # =================================================

        output = response.choices[0].message.content

        print("🤖 GROQ RESPONSE:\n")
        print(output)

        return output

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        print("\n❌ GROQ ERROR:\n")
        print(e)

        return "LLM FAILED"