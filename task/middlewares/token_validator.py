import jwt
from common_utils.token import verify_token

from task import app_config


def validate_token(token, required_scopes=None):
    public_key = app_config["PUBLIC_KEY"]
    token = token.strip()
    token_parts = token.split("Bearer")
    if len(token_parts) == 2:
        token = token[1].strip()
    data = verify_token(token, public_key)
    return {
        "scopes": data.get("scopes", "").split(","),
    }
