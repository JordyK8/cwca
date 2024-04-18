import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class GoogleAPI:
    def __init__(self):
        self.flow =  google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/youtube'])
        self.flow.redirect_uri = 'http://localhost:8000/oauth2/oauth2callback'

        def authorization_request_url():
            authorization_url, state = self.flow.authorization_url(
                # Recommended, enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                # Optional, enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true',
                # Recommended, state value can increase your assurance that an incoming connection is the result
                # of an authentication request.
                state="Some smaple string, i need to check what this does. I suspect I can give a secret to be checked later?",
                # Optional, if your application knows which user is trying to authenticate, it can use this
                # parameter to provide a hint to the Google Authentication Server.
                login_hint='hint@example.com',
                # Optional, set prompt to 'consent' will prompt the user for consent
                prompt='consent')
            
            print(authorization_url, state)
            return authorization_url
        
