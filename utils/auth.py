from google.cloud import secretmanager


def get_secret(secret_name: str) -> str:
    """
    Fetch a secret value from Google Secret Manager.
    secret_name = full resource ID, e.g.:
    "projects/123456789/secrets/YOUTUBE_API_KEY/versions/latest"
    """

    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_name})
    secret_value = response.payload.data.decode("utf-8")

    return secret_value
