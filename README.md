# gcp_oauth_phishing_example

This is an example of how to use Google Cloud Platform OAuth to phish users with an OAuth consent screen.

## Setup

You can find more info of about how to do the setup in GCP in https://cloud.hacktricks.xyz/pentesting-cloud/workspace-security/gws-google-platforms-phishing#create-an-oauth-app. However, here is a summary:

- First of all you need to create an OAuth Client ID in GCP. Note that for more impact these are the scopes the application is going to be asking the user: `https://www.googleapis.com/auth/cloud-platform, https://www.googleapis.com/auth/admin.directory.user.readonly`. So, when you crate the OAuth application you need to add these scopes to the OAuth consent screen.

- Then, you need to `generate credentials for a web application` that will use the previously created OAuth CLient ID (client id and client secret). Set the redirect url to `http://localhost:8000/callback`

- With the cli

With this info you can now run the script:

```bash
# Install requirements
pip install flask requests google-auth-oauthlib
# Run app
python3 app.py --client-id "<client_id>" --client-secret "<client_secret>"
```