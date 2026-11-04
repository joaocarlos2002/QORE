import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ServerSettings:
    host: str = "127.0.0.1"
    port: int = 0

    @classmethod
    def from_environment(cls) -> "ServerSettings":
        host = os.environ.get("QORE_API_HOST", "127.0.0.1")
        if host != "127.0.0.1":
            raise ValueError("QORE_API_HOST must be 127.0.0.1")

        raw_port = os.environ.get("QORE_API_PORT", "0")
        try:
            port = int(raw_port)
        except ValueError as exc:
            raise ValueError("QORE_API_PORT must be an integer") from exc
        if not 0 <= port <= 65535:
            raise ValueError("QORE_API_PORT must be between 0 and 65535")
        return cls(host=host, port=port)
