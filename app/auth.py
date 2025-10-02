# app/auth.py

import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
# For development only: allow OAuth2 over HTTP (not HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Load environment variables from .env file
load_dotenv()

auth_router = APIRouter()

# This is the file you downloaded from the Google Cloud Console
CLIENT_SECRETS_FILE = "client_secret.json"

# This is the scope we will request. It allows us to manage users.
# For a full list of scopes, see the Google Admin SDK documentation.
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]


@auth_router.get("/auth/login")
async def login_to_google():
    """
    Endpoint to start the OAuth 2.0 login flow.
    It creates the authorization URL and redirects the user to Google.
    """
    # Create a Flow instance from the client secrets file
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

    # Generate the authorization URL that the user will be redirected to
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Redirect the user's browser to the generated Google auth URL
    return RedirectResponse(authorization_url)


@auth_router.get("/auth/callback")
async def auth_callback(request: Request):
    """
    Endpoint that Google redirects to after the user grants permission.
    It exchanges the authorization code for an access token.
    """
    # The full URL of the request is needed to process the callback
    full_url = str(request.url)

    # We need to use the same Flow instance and redirect_uri as in the login step
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

    # Use the full URL from the request to fetch the OAuth 2.0 tokens.
    flow.fetch_token(authorization_response=full_url)

    # The 'credentials' object now holds the access token and refresh token.
    credentials = flow.credentials

    # 🔑 In a real application, you would now securely save these credentials
    # (specifically credentials.to_json()) to your PostgreSQL database,
    # associating them with the logged-in user or their organization.

    # For now, we'll just return a success message.
    return {
        "message": "Authentication successful! Credentials received.",
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_in": credentials.expiry.isoformat(),
    }