import os
from dotenv import load_dotenv


load_dotenv()
MS_URLS = {
    'AUTH_SERVICE_URL': os.getenv('AUTH_SERVICE_URL', 'http://localhost:8002'),
    'VAULT_SERVICE_URL': os.getenv('VAULT_SERVICE_URL', 'http://localhost:8003')
}
