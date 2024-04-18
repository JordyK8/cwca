import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
from typing import Dict, Optional

# Replace with your actual client secrets file path
CLIENT_SECRETS_FILE = "client_secret_435935125208.json"

# OAuth 2.0 scopes for read-only access to Youtube Analytics
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Dependency for checking if credentials are available

router = APIRouter(
    prefix="/oauth2",
    tags=["oauth2"],
    responses={404: {"description": "Not found"}},
)


@router.get('/')
async def home(request: Request):
    user = request.session.get('user')
    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@router.get("/test")
def test_api_request(request: Request):
      print('request.session', request.session) 
      if 'credentials' not in request.session:
        return request.redirect('authorize')

      # Load credentials from the session.
      credentials = google.oauth2.credentials.Credentials(
          **request.session['credentials'])

      youtube = googleapiclient.discovery.build(
          API_SERVICE_NAME, API_VERSION, credentials=credentials)

      print('youtube', youtube)
      channel = youtube.channels().list(mine=True, part='snippet,contentDetails,statistics').execute()

      # Save credentials back to session in case access token was refreshed.
      # ACTION ITEM: In a production app, you likely want to save these
      #              credentials in a persistent database instead.
      request.session['credentials'] = credentials_to_dict(credentials)
      print('channel', channel)
      return channel


@router.get("/authorize")
async def authorize(request: Request):
  # Create flow instance for OAuth 2.0 authorization
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES
  )

  # Redirect URI configured in Google API Console
  flow.redirect_uri = 'http://localhost:8000/oauth2/oauth2callback'

  # Enable offline access and incremental authorization
  authorization_url, state = flow.authorization_url(
      access_type='offline', include_granted_scopes='true', prompt='consent', state="this is some state",login_hint='hint@example.com'
  )

  # Store state for verification in the callback
  request.session["state"] = state
  return {"redirect_url": authorization_url}


@router.get("/oauth2callback")
async def oauth2callback(request: Request):
  # Get state from session
  print('request.session', request.session)
  state = request.session.get("state")

  # Create flow instance with state for verification
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
  )
  flow.redirect_uri = 'http://localhost:8000/oauth2/oauth2callback'

  # Fetch token from authorization response
  authorization_response = str(request.url)

  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials as a dictionary
  credentials_dict = credentials_to_dict(flow.credentials)
  request.session["credentials"] = credentials_dict

  return {"message": "Credentials stored successfully"}


@router.get("/revoke")
async def revoke(request: Request):
  credentials = google.oauth2.credentials.Credentials(
          **request.session['credentials'])
  revoke = requests.post(
      'https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers={'content-type': 'application/x-www-form-urlencoded'},
  )

  if revoke.status_code == 200:
    return {"message": "Credentials revoked successfully"}
  else:
    return {"message": "An error occurred"}


@router.get("/clear")
async def clear_credentials(request: Request):
  if "credentials" in request.session:
    del request.session["credentials"]
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
