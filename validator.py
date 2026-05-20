import json
import re

from pydantic import BaseModel, ValidationError
from jsonschema import validate
from rapidfuzz import fuzz


# =========================================================
# PYDANTIC MODEL
# =========================================================

class Transaction(BaseModel):

    customer_name: str
    account_number: str
    transaction_id: str
    transaction_date: str
    amount: float
    currency: str
    transaction_type: str
    merchant_name: str
    invoice_id: str
    payment_method: str
    status: str


# =========================================================
# JSON SCHEMA
# =========================================================

transaction_schema = {

    "type": "array",

    "items": {

        "type": "object",

        "required": [
            "customer_name",
            "account_number",
            "transaction_id",
            "transaction_date",
            "amount",
            "currency",
            "transaction_type",
            "merchant_name",
            "invoice_id",
            "payment_method",
            "status"
        ]
    }
}


# =========================================================
# VALIDATOR FUNCTION
# =========================================================

def validate_data(email_text, data):

    try:

        # =================================================
        # CLEAN RAW LLM OUTPUT
        # =================================================

        cleaned_data = (
            data.replace("```json", "")
                .replace("```", "")
                .strip()
        )

        # =================================================
        # CONVERT STRING TO JSON
        # =================================================

        parsed = json.loads(cleaned_data)

        # =================================================
        # ENSURE JSON ARRAY
        # =================================================

        if not isinstance(parsed, list):

            return {
                "status": "invalid",
                "error": "Expected JSON array"
            }

        # =================================================
        # JSON SCHEMA VALIDATION
        # =================================================

        validate(
            instance=parsed,
            schema=transaction_schema
        )

        validated_transactions = []

        # =================================================
        # VALIDATE EACH TRANSACTION
        # =================================================

        for idx, transaction in enumerate(parsed):

            # =============================================
            # EMPTY VALUE CHECK
            # =============================================

            for key, value in transaction.items():

                if value is None or str(value).strip() == "":

                    return {
                        "status": "invalid",
                        "error": f"Empty value found in '{key}'",
                        "failed_field": key,
                        "current_value": value,
                        "transaction_index": idx
                    }

            # =============================================
            # PYDANTIC VALIDATION
            # =============================================

            validated = Transaction(**transaction)

            cleaned_transaction = validated.dict()

            # =============================================
            # CLEAN STRING VALUES
            # =============================================

            for key, value in cleaned_transaction.items():

                if isinstance(value, str):

                    cleaned_transaction[key] = value.strip()

            # =============================================
            # REGEX VALIDATION
            # =============================================

            if not re.match(
                r"^[A-Za-z0-9_-]+$",
                cleaned_transaction["transaction_id"]
            ):

                return {
                    "status": "invalid",
                    "error": "Invalid transaction_id format",
                    "failed_field": "transaction_id",
                    "current_value": cleaned_transaction[
                        "transaction_id"
                    ],
                    "transaction_index": idx
                }

            # =============================================
            # RAPIDFUZZ VALIDATION
            # =============================================

            customer_score = fuzz.partial_ratio(
                cleaned_transaction[
                    "customer_name"
                ].lower(),
                email_text.lower()
            )

            merchant_score = fuzz.partial_ratio(
                cleaned_transaction[
                    "merchant_name"
                ].lower(),
                email_text.lower()
            )

            transaction_score = fuzz.partial_ratio(
                cleaned_transaction[
                    "transaction_id"
                ].lower(),
                email_text.lower()
            )

            # =============================================
            # CUSTOMER NAME VALIDATION
            # =============================================

            if customer_score < 70:

                return {
                    "status": "invalid",
                    "error": "Customer name mismatch",
                    "failed_field": "customer_name",
                    "current_value": cleaned_transaction[
                        "customer_name"
                    ],
                    "similarity_score": customer_score,
                    "transaction_index": idx
                }

            # =============================================
            # MERCHANT NAME VALIDATION
            # =============================================

            if merchant_score < 70:

                return {
                    "status": "invalid",
                    "error": "Merchant name mismatch",
                    "failed_field": "merchant_name",
                    "current_value": cleaned_transaction[
                        "merchant_name"
                    ],
                    "similarity_score": merchant_score,
                    "transaction_index": idx
                }

            # =============================================
            # TRANSACTION ID VALIDATION
            # =============================================

            if transaction_score < 70:

                return {
                    "status": "invalid",
                    "error": "Transaction ID mismatch",
                    "failed_field": "transaction_id",
                    "current_value": cleaned_transaction[
                        "transaction_id"
                    ],
                    "similarity_score": transaction_score,
                    "transaction_index": idx
                }

            # =============================================
            # AMOUNT RAPIDFUZZ VALIDATION
            # =============================================

            amount_text = str(
                cleaned_transaction["amount"]
            )

            clean_email = (
                email_text.replace(",", "")
            )

            amount_score = fuzz.partial_ratio(
                amount_text,
                clean_email
            )

            # =============================================
            # AMOUNT VALIDATION
            # =============================================

            if amount_score < 60:

                return {
                    "status": "invalid",
                    "error": (
                        "Amount mismatch "
                        "with source email"
                    ),
                    "failed_field": "amount",
                    "current_value": cleaned_transaction[
                        "amount"
                    ],
                    "similarity_score": amount_score,
                    "transaction_index": idx
                }

            # =============================================
            # SAVE VALID TRANSACTION
            # =============================================

            validated_transactions.append(
                cleaned_transaction
            )

        # =================================================
        # SUCCESS
        # =================================================

        return {
            "status": "valid",
            "validated_count": len(
                validated_transactions
            ),
            "data": validated_transactions
        }

    # =====================================================
    # PYDANTIC ERROR
    # =====================================================

    except ValidationError as ve:

        return {
            "status": "invalid",
            "validation_error": ve.errors()
        }

    # =====================================================
    # JSON ERROR
    # =====================================================

    except json.JSONDecodeError as je:

        return {
            "status": "invalid",
            "json_error": str(je)
        }

    # =====================================================
    # OTHER ERRORS
    # =====================================================

    except Exception as e:

        return {
            "status": "invalid",
            "error": str(e)
        }