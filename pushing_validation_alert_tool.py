# =========================================================
# PUSH VALIDATION ALERT TOOL
# =========================================================

import httpx


# =========================================================
# BASE URL
# =========================================================

BASE_URL = (
    "https://remarkable-harmony-production-2112.up.railway.app"
)


# =========================================================
# ALERT API URL
# =========================================================

ALERT_API_URL = (
    f"{BASE_URL}/api/alerts"
)


# =========================================================
# PUSH VALIDATION ALERT TOOL
# =========================================================

def push_validation_alert_tool(

    token,

    alert_payload
):

    print(
        "\nPUSHING VALIDATION ALERT TO UI...\n"
    )

    try:

        # =================================================
        # AUTH HEADERS
        # =================================================

        headers = {

            "Authorization": (
                f"Bearer {token}"
            ),

            "Content-Type":
            "application/json"
        }

        # =================================================
        # SEND ALERT
        # =================================================

        response = httpx.post(

            ALERT_API_URL,

            headers=headers,

            json=alert_payload,

            timeout=30.0
        )

        # =================================================
        # RESPONSE LOGS
        # =================================================

        print(
            "ALERT RESPONSE:",
            response.status_code
        )

        print(response.text)

        # =================================================
        # FAILURE CHECK
        # =================================================

        if response.status_code not in [
            200,
            201
        ]:

            raise Exception(

                f"ALERT PUSH FAILED → "

                f"{response.status_code} "

                f"→ {response.text}"
            )

        # =================================================
        # SUCCESS
        # =================================================

        print(
            "\nVALIDATION ALERT "
            "PUSHED SUCCESSFULLY\n"
        )

        return {

            "status": "success"
        }

    # =====================================================
    # EXCEPTION HANDLING
    # =====================================================

    except Exception as e:

        print(
            "\nVALIDATION ALERT "
            "PUSH FAILED\n"
        )

        print(e)

        return {

            "status": "failed",

            "error": str(e)
        }