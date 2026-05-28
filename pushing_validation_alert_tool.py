# =========================================================
# PUSH VALIDATION ALERT TOOL
# =========================================================

import httpx


def push_validation_alert_tool(

    token,

    alert_payload
):

    print(
        "\nPUSHING VALIDATION ALERT TO UI...\n"
    )

    try:

        # =================================================
        # ALERT API ENDPOINT
        # =================================================

        ALERT_API_URL = (
            "https://content-nature-production-fefe.up.railway.app/api/alerts"
        )

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

        print(
            "\nVALIDATION ALERT "
            "PUSHED SUCCESSFULLY\n"
        )

        return {

            "status": "success"
        }

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