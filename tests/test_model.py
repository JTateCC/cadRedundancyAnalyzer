# tests/test_model.py
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature

class TestComponentMetadata:

    def test_component_metadata_creation_with_required_fields(self):
        """Test creating ComponentMetadata with minimum required fields"""
        metadata = ComponentMetadata(
            file_path="/projects/bracket.stl",
            file_name="bracket.stl",
            project_id="ProjectA"
        )
        assert metadata.file_path == "/projects/bracket.stl"
        assert metadata.file_name == "bracket.stl"
        assert metadata.project_id == "ProjectA"
        # Optional fields should default to None
        assert metadata.part_number is None
        assert metadata.description is None
        assert metadata.material is None
        assert metadata.weight is None
        assert metadata.volume is None


    def test_component_metadata_with_all_fields(self):
        """Test creating ComponentMetadata with all fields populated"""
        metadata = ComponentMetadata(
            file_path="/projects/bracket.stl",
            file_name="bracket.stl",
            project_id="ProjectA",
            part_number="BRK-001",
            description="Mounting bracket",
            material="Aluminum",
            weight=0.5,
            volume=125.0,

        )
        assert metadata.part_number == "BRK-001"
        assert metadata.description == "Mounting bracket"
        assert metadata.material == "Aluminum"
        assert metadata.weight == 0.5
        assert metadata.volume == 125.0



class TestGeometricSignature:

    def test_geometric_signature_creation(self):
        """Test creating a geometric signature"""
        signature = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 10.0, 5.0, 2.0),
            volume=100.0,
            surface_area=220.0,
            geometric_hash="abc123def456"
        )
        assert signature.bounding_box == (0.0, 0.0, 0.0, 10.0, 5.0, 2.0)
        assert signature.volume == 100.0
        assert signature.surface_area == 220.0
        assert signature.geometric_hash == "abc123def456"

    def test_geometric_signature_equality(self):
        """Test when two signatures should be considered equal"""
        sig1 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 10.0, 5.0, 2.0),
            volume=100.0,
            surface_area=220.0,
            geometric_hash="abc123"
        )
        sig2 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 10.0, 5.0, 2.0),
            volume=100.0,
            surface_area=220.0,
            geometric_hash="abc123"
        )
        assert sig1 == sig2


