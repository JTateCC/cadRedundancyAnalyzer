# cadRedundancyAnalyzer/core/similarity.py
from typing import List, Tuple
from cadRedundancyAnalyzer.core.models import GeometricSignature


class SimilarityDetector:
    """Detects similar and duplicate components based on geometric signatures"""

    def calculate_similarity(self, sig1: GeometricSignature, sig2: GeometricSignature) -> float:
        """
        Calculate similarity score between two geometric signatures.
        Returns a value between 0.0 (completely different) and 1.0 (identical)
        """
        # Quick check: if hashes are identical, parts are identical
        if sig1.geometric_hash == sig2.geometric_hash:
            return 1.0

        # Calculate similarity based on volume, surface area, and bounding box
        volume_similarity = self._calculate_property_similarity(sig1.volume, sig2.volume)
        area_similarity = self._calculate_property_similarity(sig1.surface_area, sig2.surface_area)
        bbox_similarity = self._calculate_bounding_box_similarity(sig1.bounding_box, sig2.bounding_box)

        # Weighted average (volume is most important for duplicate detection)
        similarity = (
                0.5 * volume_similarity +
                0.3 * area_similarity +
                0.2 * bbox_similarity
        )

        return similarity

    def _calculate_property_similarity(self, val1: float, val2: float) -> float:
        """Calculate similarity between two numeric properties"""
        if val1 == 0 and val2 == 0:
            return 1.0

        if val1 == 0 or val2 == 0:
            return 0.0

        # Calculate percentage difference
        larger = max(val1, val2)
        smaller = min(val1, val2)
        ratio = smaller / larger

        return ratio

    def _calculate_bounding_box_similarity(self, bbox1: tuple, bbox2: tuple) -> float:
        """Calculate similarity between two bounding boxes"""
        # Calculate dimensions for each bounding box
        dims1 = (
            bbox1[3] - bbox1[0],  # width (max_x - min_x)
            bbox1[4] - bbox1[1],  # depth (max_y - min_y)
            bbox1[5] - bbox1[2]  # height (max_z - min_z)
        )
        dims2 = (
            bbox2[3] - bbox2[0],
            bbox2[4] - bbox2[1],
            bbox2[5] - bbox2[2]
        )

        # Compare each dimension
        similarities = []
        for d1, d2 in zip(dims1, dims2):
            if d1 == 0 and d2 == 0:
                similarities.append(1.0)
            elif d1 == 0 or d2 == 0:
                similarities.append(0.0)
            else:
                ratio = min(d1, d2) / max(d1, d2)
                similarities.append(ratio)

        # Average similarity across all dimensions
        return sum(similarities) / len(similarities)

    def find_duplicates(self, signatures: List[Tuple[str, GeometricSignature]],
                        threshold: float = 0.95) -> List[List[str]]:
        """
        Find groups of duplicate/similar components.

        Args:
            signatures: List of (filename, GeometricSignature) tuples
            threshold: Similarity threshold (0.0-1.0). Default 0.95 means 95% similar

        Returns:
            List of groups, where each group is a list of filenames that are similar
        """
        if not signatures:
            return []

        # Track which parts have been grouped
        grouped = set()
        duplicate_groups = []

        # Compare each part with every other part
        for i, (file1, sig1) in enumerate(signatures):
            if file1 in grouped:
                continue

            # Start a new group with this part
            current_group = [file1]

            # Find all similar parts
            for j, (file2, sig2) in enumerate(signatures):
                if i != j and file2 not in grouped:
                    similarity = self.calculate_similarity(sig1, sig2)
                    if similarity >= threshold:
                        current_group.append(file2)
                        grouped.add(file2)

            # Only add groups with duplicates (size > 1)
            if len(current_group) > 1:
                duplicate_groups.append(current_group)
                grouped.add(file1)

        return duplicate_groups