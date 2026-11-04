from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
import tempfile


_SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class StoredDocument:
    filename: str
    path: Path
    content_hash: str
    size: int


class DocumentStorage:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def store(self, filename: str, content: bytes) -> StoredDocument:
        safe_name = self._safe_filename(filename)
        content_hash = sha256(content).hexdigest()
        destination = self._confined_path(f"{content_hash}-{safe_name}")

        if not destination.exists():
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=self.root,
                prefix=".upload-",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temporary.write(content)
                temporary.flush()
                temporary_path = Path(temporary.name)
            temporary_path.replace(destination)

        return StoredDocument(
            filename=safe_name,
            path=destination,
            content_hash=content_hash,
            size=len(content),
        )

    def _confined_path(self, filename: str) -> Path:
        candidate = (self.root / filename).resolve()
        if candidate.parent != self.root:
            raise ValueError("Document path escapes the configured storage directory")
        return candidate

    @staticmethod
    def _safe_filename(filename: str) -> str:
        name = Path(filename).name
        safe_name = _SAFE_FILENAME.sub("_", name).strip(" .")
        if not safe_name or safe_name in {".", ".."}:
            raise ValueError("Document filename is invalid")
        return safe_name[:260]
