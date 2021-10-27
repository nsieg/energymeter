import onedrivesdk, logging

logger = logging.getLogger("onedrive")

class Onedrive():
    def __init__(self, props):
        self.props = props   
        self.api_base_url='https://api.onedrive.com/v1.0/'
        self.scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    def connect(self):            
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(http_provider, self.props['onedrive']['clientId'], self.scopes)

        self.__load_session(auth_provider)        
        logger.info("Loaded session from file")   
        
        logger.info("Connecting to Onedrive")   
        self.client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
    
    def upload(self, file, name, path):
        folder_id = self.client.item(drive="me", path=path).get().id
        logger.info("Uploading {0} into folder {1} ({2})".format(name, path, folder_id))
        self.client.item(drive='me', id=folder_id).children[name].upload(file)

    def __load_session(self, auth_provider):
        auth_provider.load_session()
        auth_provider.refresh_token()
