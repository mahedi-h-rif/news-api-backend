import os

CLIENT_ID = os.getenv("CLIENT_ID", "blockstak-client")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "blockstak-secret")


def verify_client_credentials(client_id: str, client_secret: str) -> bool:
    return client_id == CLIENT_ID and client_secret == CLIENT_SECRET
