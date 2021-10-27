import onedrivesdk, os, pickle, json
from onedrivesdk.helpers import GetAuthCodeServer

with open("secrets.json", "r") as f:
    props = json.load(f)

scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

try:
    os.remove("session.pickle")
except OSError:
    pass

redirect_uri = props['onedrive_redirect_uri']
client = onedrivesdk.get_default_client(props['onedrive_client_id'], scopes)
auth_url = client.auth_provider.get_auth_url(redirect_uri)
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
client.auth_provider.authenticate(code, redirect_uri, props['onedrive_client_secret'])
client.auth_provider.save_session()

v5_file = pickle.load( open( "session.pickle", "rb" ) )
with open('session.pickle', 'wb') as handle:
    pickle.dump(v5_file, handle, protocol=4)
