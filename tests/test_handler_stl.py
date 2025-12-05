# tests/test_stl_handler.py
import pytest
import sys
import os
from pathlib import Path
import tempfile
import numpy as np
from stl import mesh

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cadRedundancyAnalyzer.handlers.stl_handler import STLFileHandler
from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature


class TestSTLFileHandler:

    def test_can_handle_stl_files(self):
        """Test that handler recognizes STL files"""
        handler = STLFileHandler()

        assert handler.can_handle("bracket.stl") == True
        assert handler.can_handle("HOUSING.STL") == True
        assert handler.can_handle("part.step") == False
        assert handler.can_handle("drawing.dxf") == False

    def test_extract_metadata_from_stl_file(self):
        """Test extracting metadata from an STL file"""
        handler = STLFileHandler()

        # Create a simple test STL file (a cube)
        with tempfile.TemporaryDirectory() as temp_dir:
            stl_path = Path(temp_dir) / "test_cube.stl"

            # Create a simple cube mesh
            vertices = np.array([
                [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Bottom face
                [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]  # Top face
            ])
            faces = np.array([
                [0, 1, 2], [0, 2, 3],  # Bottom
                [4, 5, 6], [4, 6, 7],  # Top
                [0, 1, 5], [0, 5, 4],  # Front
                [2, 3, 7], [2, 7, 6],  # Back
                [0, 3, 7], [0, 7, 4],  # Left
                [1, 2, 6], [1, 6, 5]  # Right
            ])

            cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, face in enumerate(faces):
                for j in range(3):
                    cube.vectors[i][j] = vertices[face[j]]
            cube.save(str(stl_path))

            # Extract metadata
            metadata = handler.get_metadata(str(stl_path), "ProjectA")

            assert metadata.file_path == str(stl_path)

    def test_extract_geometric_signature_from_stl(self):
        """Test extracting geometric properties from STL file"""
        handler = STLFileHandler()

        # Create a simple test STL file
        with tempfile.TemporaryDirectory() as temp_dir:
            stl_path = Path(temp_dir) / "test_part.stl"

            # Create simple geometry (triangle)
            vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
            faces = np.array([[0, 1, 2]])

            triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, face in enumerate(faces):
                for j in range(3):
                    triangle.vectors[i][j] = vertices[face[j]]
            triangle.save(str(stl_path))

            # Extract geometric signature
            signature = handler.extract_geometry(str(stl_path))

            assert signature.bounding_box is not None
            assert len(signature.bounding_box) == 6  # (min_x, min_y, min_z, max_x, max_y, max_z)
            assert signature.volume >= 0
            assert signature.surface_area > 0
            assert signature.geometric_hash is not None
            assert len(signature.geometric_hash) > 0

    def test_geometric_hash_consistency(self):
        """Test that same geometry produces same hash"""
        handler = STLFileHandler()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create two identical STL files with different names
            stl_path1 = Path(temp_dir) / "part1.stl"
            stl_path2 = Path(temp_dir) / "part2.stl"

            vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
            faces = np.array([[0, 1, 2]])

            for stl_path in [stl_path1, stl_path2]:
                triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
                for i, face in enumerate(faces):
                    for j in range(3):
                        triangle.vectors[i][j] = vertices[face[j]]
                triangle.save(str(stl_path))

            # Extract signatures
            sig1 = handler.extract_geometry(str(stl_path1))
            sig2 = handler.extract_geometry(str(stl_path2))

            # Same geometry should produce same hash
            assert sig1.geometric_hash == sig2.geometric_hash
            assert sig1.volume == sig2.volume
            assert sig1.surface_area == sig2.surface_area
            assert sig1.bounding_box == sig2.bounding_box