import secrets

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class LocalAuthenticator:
    def __init__(self) -> None:
        self.token = secrets.token_urlsafe(32)
        self._scheme = HTTPBearer(auto_error=False)

    async def require_token(self, request: Request) -> None:
        credentials: HTTPAuthorizationCredentials | None = await self._scheme(request)
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not secrets.compare_digest(credentials.credentials, self.token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
