# cadRedundancyAnalyzer/core/analyzer.py
from typing import List, Dict
from pathlib import Path

from cadRedundancyAnalyzer.core.models import ComponentMetadata, GeometricSignature
from cadRedundancyAnalyzer.core.similarity import SimilarityDetector
from cadRedundancyAnalyzer.handlers.stl_handler import STLFileHandler
from cadRedundancyAnalyzer.discovery.filesystem import FileSystemCrawler


class ComponentAnalyzer:
    """Main class for analyzing CAD components and finding duplicates"""

    def __init__(self):
        self.components: List[ComponentMetadata] = []
        self.geometric_signatures: Dict[str, GeometricSignature] = {}
        self.handler = STLFileHandler()
        self.similarity_detector = SimilarityDetector()
        self.crawler = FileSystemCrawler()

    def process_file(self, file_path: str, root_path: str):
        """
        Process a single CAD file and add it to the analyzer.

        Args:
            file_path: Full path to the CAD file
            root_path: Root directory being scanned (for project extraction)
        """
        if not self.handler.can_handle(file_path):
            raise ValueError(f"Handler cannot process file: {file_path}")

        # Extract project info from path
        path = Path(file_path)
        project_id = self.crawler.extract_project_info(path, root_path)

        # Get metadata and geometric signature
        metadata = self.handler.get_metadata(file_path, project_id)
        signature = self.handler.extract_geometry(file_path)

        # Store them
        self.components.append(metadata)
        self.geometric_signatures[file_path] = signature

    def find_duplicates(self, threshold: float = 0.95) -> List[List[str]]:
        """
        Find groups of duplicate/similar components.

        Args:
            threshold: Similarity threshold (0.0-1.0). Default 0.95 means 95% similar

        Returns:
            List of duplicate groups, where each group is a list of file paths
        """
        # Create list of (filepath, signature) tuples for similarity detector
        signatures = [(filepath, sig) for filepath, sig in self.geometric_signatures.items()]

        # Use similarity detector to find duplicates
        duplicate_groups = self.similarity_detector.find_duplicates(signatures, threshold)

        return duplicate_groups

    def scan_directory(self, root_path: str):
        """
        Scan an entire directory for CAD files and process them all.

        Args:
            root_path: Root directory to scan
        """
        for cad_file in self.crawler.discover_files(root_path):
            try:
                self.process_file(str(cad_file), root_path)
            except Exception as e:
                # Log error but continue processing other files
                print(f"Error processing {cad_file}: {e}")