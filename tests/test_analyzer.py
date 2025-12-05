# tests/test_analyzer.py
import pytest
import sys
import os
from pathlib import Path
import tempfile
import numpy as np
from stl import mesh

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cadRedundancyAnalyzer.core.analyzer import ComponentAnalyzer
from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature


class TestComponentAnalyzer:

    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly"""
        analyzer = ComponentAnalyzer()

        assert analyzer is not None
        assert len(analyzer.components) == 0
        assert len(analyzer.geometric_signatures) == 0

    def test_process_file_adds_component(self):
        """Test that processing a file adds it to the analyzer"""
        analyzer = ComponentAnalyzer()

        # Create a simple STL file
        with tempfile.TemporaryDirectory() as temp_dir:
            stl_path = Path(temp_dir) / "bracket.stl"

            # Create simple triangle
            vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
            faces = np.array([[0, 1, 2]])

            triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, face in enumerate(faces):
                for j in range(3):
                    triangle.vectors[i][j] = vertices[face[j]]
            triangle.save(str(stl_path))

            # Process the file
            analyzer.process_file(str(stl_path), temp_dir)

            # Should have one component
            assert len(analyzer.components) == 1
            assert len(analyzer.geometric_signatures) == 1

            # Check component data
            component = analyzer.components[0]
            assert component.file_name == "bracket.stl"
            assert component.project_id is not None

    def test_process_multiple_files(self):
        """Test processing multiple files"""
        analyzer = ComponentAnalyzer()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create multiple STL files
            for i in range(3):
                stl_path = Path(temp_dir) / f"part{i}.stl"
                vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
                faces = np.array([[0, 1, 2]])

                triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
                for j, face in enumerate(faces):
                    for k in range(3):
                        triangle.vectors[j][k] = vertices[face[k]]
                triangle.save(str(stl_path))

                analyzer.process_file(str(stl_path), temp_dir)

            # Should have three components
            assert len(analyzer.components) == 3
            assert len(analyzer.geometric_signatures) == 3

    def test_find_duplicates_identifies_identical_parts(self):
        """Test that find_duplicates identifies identical parts"""
        analyzer = ComponentAnalyzer()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create two identical STL files with different names
            vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
            faces = np.array([[0, 1, 2]])

            for name in ["part1.stl", "part2.stl", "part3.stl"]:
                stl_path = Path(temp_dir) / name
                triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
                for i, face in enumerate(faces):
                    for j in range(3):
                        triangle.vectors[i][j] = vertices[face[j]]
                triangle.save(str(stl_path))

                analyzer.process_file(str(stl_path), temp_dir)

            # Find duplicates
            duplicates = analyzer.find_duplicates(threshold=0.95)

            # Should find one group with all 3 parts
            assert len(duplicates) >= 1

            # Check that we found the duplicates
            largest_group = max(duplicates, key=lambda g: len(g))
            assert len(largest_group) == 3

    def test_find_duplicates_with_different_threshold(self):
        """Test that threshold affects duplicate detection"""
        analyzer = ComponentAnalyzer()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create slightly different parts
            for i, scale in enumerate([1.0, 1.02, 1.05]):  # 0%, 2%, 5% larger
                stl_path = Path(temp_dir) / f"part{i}.stl"
                vertices = np.array([[0, 0, 0], [scale, 0, 0], [0, scale, 0]])
                faces = np.array([[0, 1, 2]])

                triangle = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
                for j, face in enumerate(faces):
                    for k in range(3):
                        triangle.vectors[j][k] = vertices[face[k]]
                triangle.save(str(stl_path))

                analyzer.process_file(str(stl_path), temp_dir)

            # High threshold (99%) - should find fewer duplicates
            strict_duplicates = analyzer.find_duplicates(threshold=0.99)

            # Lower threshold (90%) - should find more duplicates
            loose_duplicates = analyzer.find_duplicates(threshold=0.90)

            # Loose threshold should find same or more duplicates
            assert len(loose_duplicates) >= len(strict_duplicates)