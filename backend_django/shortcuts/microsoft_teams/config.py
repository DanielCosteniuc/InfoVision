# microsoft_teams/config.py
MSAL_CONFIG = {
    "client_id": "51624ba1-4a00-43c7-b5f1-2500ac4d5591",
    "client_secret": "2AC8Q~LUAxEBo5YFO~PL5s9hnpX6lmGkvVQEaa2a",
    "authority": "https://login.microsoftonline.com/37c00ed0-e757-4283-b0be-82c4b1c08f4c",  # Tenant ID
    "redirect_uri": "http://localhost:3000/shortcuts/teams",  # URI-ul din manifest
    "scope": ["User.Read", "Contacts.Read"]
}
