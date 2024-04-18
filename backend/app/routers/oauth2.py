import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from typing import Dict, Optional

# Replace with your actual client secrets file path
CLIENT_SECRETS_FILE = "client_secret.json"

# OAuth 2.0 scopes for read-only access to Youtube Analytics
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v1'

# Dependency for checking if credentials are available
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=None)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

async def get_credentials(token: Optional[str] = Depends(oauth2_scheme)):
  if not token:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No credentials provided",
    )
  return Credentials(**token)

@router.get("/", response_class=HTMLResponse)
async def index():
  return print_index_table()

@router.get("/test")
async def test_api_request(credentials: Credentials = Depends(get_credentials)):
  youtube = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials
  )
  report = youtube.reports().query(
      ids='channel==MINE', start_date='2016-05-01', end_date='2016-06-30', metrics='views'
  ).execute()
  return report


@router.get("/authorize")
async def authorize():
  # Create flow instance for OAuth 2.0 authorization
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES
  )

  # Redirect URI configured in Google API Console
  flow.redirect_uri = router.url_path_for("oauth2callback")

  # Enable offline access and incremental authorization
  authorization_url, state = flow.authorization_url(
      access_type='offline', include_granted_scopes='true'
  )

  # Store state for verification in the callback
  app.session["state"] = state
  return {"redirect_url": authorization_url}


@router.get("/oauth2callback")
async def oauth2callback():
  # Get state from session
  state = app.session.get("state")

  # Create flow instance with state for verification
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
  )
  flow.redirect_uri = app.url_path_for("oauth2callback")

  # Fetch token from authorization response
  authorization_response = app.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials as a dictionary
  credentials_dict = credentials_to_dict(flow.credentials)
  app.session["credentials"] = credentials_dict

  return {"message": "Authorization successful"}


@router.get("/revoke")
async def revoke(credentials: Credentials = Depends(get_credentials)):
  revoke = requests.post(
      'https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers={'content-type': 'application/x-www-form-urlencoded'},
  )

  if revoke.status_code == 200:
    return {"message": "Credentials revoked successfully"} + print_index_table()
  else:
    return {"message": "An error occurred"} + print_index_table()


@router.get("/clear")
async def clear_credentials():
  if "credentials" in app.session:
    del app.session["credentials"]
  return {"message": "Credentials cleared"} + print_index_table()


def credentials_to_dict(credentials: Credentials) -> Dict:
  return {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes}

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')
