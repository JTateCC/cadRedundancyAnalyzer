from dataclasses import dataclass
from typing import List, Dict, Optional
@dataclass
class ComponentMetadata:
    """Basic component information"""
    file_path: str
    file_name: str
    project_id: str
    part_number: Optional[str] = None
    description: Optional[str] = None
    material: Optional[str] = None
    weight: Optional[float] = None
    volume: Optional[float] = None


@dataclass
class GeometricSignature:
    """Geometric fingerprint for similarity detection"""
    bounding_box: tuple  # (min_x, min_y, min_z, max_x, max_y, max_z)
    volume: float
    surface_area: float
    geometric_hash: str  # For quick comparison
