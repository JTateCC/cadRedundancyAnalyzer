from abc import ABC, abstractmethod



class CADFileHandler(ABC):
    """Abstract base for different CAD format handlers"""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this handler supports the file format"""
        pass

    @abstractmethod
    def extract_geometry(self, file_path: str) -> GeometricSignature:
        """Extract geometric data from the CAD file"""
        pass

    @abstractmethod
    def get_metadata(self, file_path: str) -> ComponentMetadata:
        """Extract metadata from the CAD file"""
        pass