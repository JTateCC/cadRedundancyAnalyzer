from pathlib import Path
from typing import Generator, List


class FileSystemCrawler:
    """Discovers CAD files in directory structures"""

    def __init__(self, supported_extensions: List[str] = None):
        """Initialize crawler with supported file extensions"""
        # Default to STL extensions if none provided
        self.supported_extensions = supported_extensions or ['.stl']

    def discover_files(self, root_path: str) -> Generator[Path, None, None]:
        """Recursively find all CAD files under root_path"""
        root = Path(root_path)

        # Recursively walk through all files
        for file_path in root.rglob('*'):
            if file_path.is_file() and self._is_cad_file(file_path):
                yield file_path
    def _is_cad_file(self, file_path: Path) -> bool:
        """Check if file extension indicates CAD file"""
        return file_path.suffix.lower() in self.supported_extensions

    def extract_project_info(self, file_path: Path, root_path: str) -> str:
        """Try to infer project from directory structure"""
        try:
            # Get path relative to root
            relative_path = file_path.relative_to(root_path)
            parts = relative_path.parts

            # Assume first directory under root is project name
            return parts[0] if len(parts) > 1 else "Unknown"
        except (ValueError, IndexError):
            return "Unknown"



