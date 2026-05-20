print(" ui_agent imported")

import json
import pandas as pd
import httpx

# ==============================
# FRONTEND CONFIG
# ==============================

BASE_URL = "https://content-nature-production-fefe.up.railway.app"

LOGIN_API_URL = f"{BASE_URL}/api/agent/login"
UPLOAD_API_URL = f"{BASE_URL}/api/agent/upload"

EMAIL = "agentmailak44@gmail.com"
PASSWORD = "AgentPassword4382"


# ==============================
# TOOL 1 → SAVE JSON
# ==============================

def save_json_tool(validated_data):

    formatted_data = json.dumps(validated_data, indent=4)

    with open("verified_data.json", "w") as f:
        f.write(formatted_data)

    print(" VERIFIED DATA SAVED AS JSON")


# ==============================
# TOOL 2 → GENERATE EXCEL
# ==============================

def generate_excel_tool(validated_data):

    excel_data = validated_data["data"]

    df = pd.DataFrame(excel_data)

    df.to_excel("verified_data.xlsx", index=False)

    print(" VERIFIED DATA SAVED AS EXCEL")


# ==============================
# TOOL 3 → LOGIN TOOL
# ==============================

def login_tool():

    login_response = httpx.post(
        LOGIN_API_URL,
        json={
            "email": EMAIL,
            "password": PASSWORD
        }
    )

    print(" LOGIN RESPONSE:", login_response.status_code)
    print(login_response.text)

    # LOGIN FAILED
    if login_response.status_code != 200:

        raise Exception(
            f"LOGIN FAILED → {login_response.status_code} → {login_response.text}"
        )

    # GET TOKEN
    token = login_response.json()["access_token"]

    print(" LOGIN SUCCESSFUL")

    return token


# ==============================
# TOOL 4 → UPLOAD TOOL
# ==============================

def upload_tool(token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    with open("verified_data.xlsx", "rb") as f:

        response = httpx.post(
            UPLOAD_API_URL,
            headers=headers,
            files={
                "file": (
                    "verified_data.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            },
            timeout=120.0
        )

    print(" UPLOAD RESPONSE:", response.status_code)
    print(response.text)

    # UPLOAD FAILED
    if response.status_code != 200:

        raise Exception(
            f"UPLOAD FAILED → {response.status_code} → {response.text}"
        )

    print(" FILE SUCCESSFULLY PUSHED TO FRONTEND")


# ==============================
# MAIN UI AGENT
# ==============================

def push_to_ui(validated_data):

    print("\n PUSHING VERIFIED DATA TO UI...\n")

    try:

        # STEP 1 → SAVE JSON
        save_json_tool(validated_data)

        # STEP 2 → GENERATE EXCEL
        generate_excel_tool(validated_data)

        # STEP 3 → LOGIN
        token = login_tool()

        # STEP 4 → UPLOAD FILE
        upload_tool(token)

        return {
            "status": "success",
            "message": "Data pushed successfully to frontend"
        }

    except Exception as e:

        print("\n UI AGENT ERROR:")
        print(e)

        return {
            "status": "failed",
            "error": str(e)
        }