# tests/test_similarity.py
import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cadRedundancyAnalyzer.core.similarity import SimilarityDetector
from cadRedundancyAnalyzer.core.models import GeometricSignature


class TestSimilarityDetector:

    def test_exact_match_returns_100_percent_similarity(self):
        """Test that identical geometries return 100% similarity"""
        detector = SimilarityDetector()

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

        similarity = detector.calculate_similarity(sig1, sig2)
        assert similarity == 1.0  # 100% match

    def test_same_hash_returns_100_percent_similarity(self):
        """Test that same geometric hash means identical parts"""
        detector = SimilarityDetector()

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

        similarity = detector.calculate_similarity(sig1, sig2)
        assert similarity == 1.0

    def test_completely_different_parts_low_similarity(self):
        """Test that very different parts have low similarity"""
        detector = SimilarityDetector()

        # Small part
        sig1 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 1.0, 1.0, 1.0),
            volume=1.0,
            surface_area=6.0,
            geometric_hash="abc123"
        )
        # Large part
        sig2 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 100.0, 100.0, 100.0),
            volume=1000000.0,
            surface_area=60000.0,
            geometric_hash="xyz789"
        )

        similarity = detector.calculate_similarity(sig1, sig2)
        assert similarity < 0.5  # Less than 50% similar

    def test_similar_but_not_identical_parts(self):
        """Test parts that are similar but not exact matches"""
        detector = SimilarityDetector()

        # Part with slight variation (maybe different tolerance/manufacturing)
        sig1 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 10.0, 5.0, 2.0),
            volume=100.0,
            surface_area=220.0,
            geometric_hash="abc123"
        )
        sig2 = GeometricSignature(
            bounding_box=(0.0, 0.0, 0.0, 10.1, 5.1, 2.0),  # Slightly different
            volume=102.0,  # 2% larger
            surface_area=224.0,
            geometric_hash="abc456"  # Different hash due to slight difference
        )

        similarity = detector.calculate_similarity(sig1, sig2)
        assert similarity > 0.9  # Should be highly similar (>90%)
        assert similarity < 1.0  # But not identical

    def test_find_duplicates_groups_similar_parts(self):
        """Test that find_duplicates groups similar parts together"""
        detector = SimilarityDetector()

        # Create a list of signatures with some duplicates
        signatures = [
            ("part1.stl", GeometricSignature((0, 0, 0, 10, 5, 2), 100.0, 220.0, "hash1")),
            ("part2.stl", GeometricSignature((0, 0, 0, 10, 5, 2), 100.0, 220.0, "hash1")),  # Duplicate of part1
            ("part3.stl", GeometricSignature((0, 0, 0, 20, 10, 4), 400.0, 880.0, "hash2")),
            ("part4.stl", GeometricSignature((0, 0, 0, 10, 5, 2), 100.0, 220.0, "hash1")),  # Another duplicate
        ]

        duplicate_groups = detector.find_duplicates(signatures, threshold=0.95)

        # Should find one group with 3 duplicates (part1, part2, part4)
        assert len(duplicate_groups) >= 1

        # The largest group should have 3 parts
        largest_group = max(duplicate_groups, key=len)
        assert len(largest_group) == 3