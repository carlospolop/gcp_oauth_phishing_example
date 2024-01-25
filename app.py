from flask import Flask, request, session, render_template_string
from google_auth_oauthlib.flow import Flow
import os
import argparse

# Parse CLI arguments
parser = argparse.ArgumentParser(description='Run the Flask app with Google OAuth.')
parser.add_argument('--client-id', required=True, help='Google Client ID')
parser.add_argument('--client-secret', required=True, help='Google Client Secret')
parser.add_argument('--redir-url', default='http://localhost:8000/callback', help='URL for redirect. By default: http://localhost:8000/callback')
args = parser.parse_args()

# Configuration
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # ONLY for development
GOOGLE_CLIENT_ID = args.client_id
GOOGLE_CLIENT_SECRET = args.client_secret
REDIRECT_URI = args.redir_url

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Define the OAuth2 flow
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID ,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
            "scopes": ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/admin.directory.user.readonly"]
        }
    },
    scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/admin.directory.user.readonly"],
    redirect_uri=REDIRECT_URI
)

@app.route('/')
def index():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return render_template_string("""
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .button {
                    display: inline-block;
                    background: #4285F4;
                    color: white;
                    border-radius: 2px;
                    padding: 10px 20px;
                    font-size: 16px;
                    text-decoration: none;
                    -webkit-box-shadow: 0 3px 6px 0 #666;
                    box-shadow: 0 3px 6px 0 #666;
                }
                .button:hover {
                    background: #357ae8;
                }
                .button img {
                    vertical-align: middle;
                    margin-right: 8px;
                }
            </style>
        </head>
        <body>
            <a href="{{ authorization_url }}" class="button">
                <img src="https://www.google.com/favicon.ico" alt="Google logo">
                <b>Login with Google</b>
            </a>
        </body>
    </html>
    """, authorization_url=authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        return "State does not match!", 400
    
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return f'Credentials: {session["credentials"]}'

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run('localhost', 8000)