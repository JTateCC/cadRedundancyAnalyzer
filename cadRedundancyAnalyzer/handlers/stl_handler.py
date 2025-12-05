from pathlib import Path
import trimesh
from cadRedundancyAnalyzer.handlers.base import CADFileHandler
from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature
class STLFileHandler(CADFileHandler):
    def can_handle(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == '.stl'

    def extract_geometry(self, file_path: str) -> GeometricSignature:
        from pathlib import Path
import trimesh
import hashlib
from cadRedundancyAnalyzer.handlers.base import CADFileHandler
from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature


class STLFileHandler(CADFileHandler):
    def can_handle(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == '.stl'

    def get_metadata(self, file_path: str, project_id: str) -> ComponentMetadata:
        """Extract metadata from STL file"""
        path = Path(file_path)

        # Load the mesh to get volume
        mesh = trimesh.load_mesh(str(file_path))

        # Create metadata with basic file info and calculated volume
        metadata = ComponentMetadata(
            file_path=str(file_path),
            file_name=path.name,
            project_id=project_id,
            volume=float(mesh.volume) if mesh.volume else 0.0
        )

        return metadata

    def extract_geometry(self, file_path: str) -> GeometricSignature:
        """Extract geometric properties from STL file"""
        # Load the mesh
        mesh = trimesh.load_mesh(str(file_path))

        # Calculate bounding box (min_x, min_y, min_z, max_x, max_y, max_z)
        bounds = mesh.bounds  # Returns [[min_x, min_y, min_z], [max_x, max_y, max_z]]
        bounding_box = (
            float(bounds[0][0]), float(bounds[0][1]), float(bounds[0][2]),
            float(bounds[1][0]), float(bounds[1][1]), float(bounds[1][2])
        )

        # Calculate volume and surface area
        volume = float(mesh.volume) if mesh.volume else 0.0
        surface_area = float(mesh.area) if mesh.area else 0.0

        # Generate geometric hash based on key properties
        # This creates a fingerprint for similarity comparison
        hash_string = f"{volume:.6f}_{surface_area:.6f}_{bounding_box}"
        geometric_hash = hashlib.md5(hash_string.encode()).hexdigest()

        return GeometricSignature(
            bounding_box=bounding_box,
            volume=volume,
            surface_area=surface_area,
            geometric_hash=geometric_hash
        )

    def get_metadata(self, file_path: str, project_id: str) -> ComponentMetadata:
        path = Path(file_path)

        # Load the mesh to get volume
        mesh = trimesh.load_mesh(str(file_path))

        # Create metadata with basic file info and calculated volume
        metadata = ComponentMetadata(
            file_path=str(file_path),
            file_name=path.name,
            project_id=project_id,
            volume=float(mesh.volume) if mesh.volume else 0.0
        )

        return metadata
