# app/auth.py

import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

# For development only: allowing OAuth2 over HTTP (not HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv()

auth_router = APIRouter()

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]


@auth_router.get("/auth/login")
async def login_to_google():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return RedirectResponse(authorization_url)


@auth_router.get("/auth/callback")
async def auth_callback(request: Request):
    full_url = str(request.url)

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

    flow.fetch_token(authorization_response=full_url)

    credentials = flow.credentials

    # Will save these credentials
    # specifically credentials.to_json() to database,
    # associating them with the logged-in user or their orgs.

    # Success test message
    return {
        "message": "Authentication successful! Credentials received.",
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_in": credentials.expiry.isoformat(),
    }