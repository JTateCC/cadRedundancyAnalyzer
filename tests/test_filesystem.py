# tests/test_filesystem.py
import pytest
import sys
import os
from pathlib import Path
import tempfile

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cadRedundancyAnalyzer.discovery.filesystem import FileSystemCrawler


class TestFileSystemCrawler:

    def test_crawler_initialization_with_default_extensions(self):
        """Test that crawler initializes with default STL extensions"""
        crawler = FileSystemCrawler()

        # Should include STL extensions
        assert '.stl' in crawler.supported_extensions

    def test_crawler_initialization_with_custom_extensions(self):
        """Test that crawler accepts custom file extensions"""
        custom_extensions = ['.stl', '.obj', '.ply']
        crawler = FileSystemCrawler(supported_extensions=custom_extensions)

        assert crawler.supported_extensions == custom_extensions

    def test_is_cad_file_recognizes_stl_files(self):
        """Test that _is_cad_file correctly identifies STL files"""
        crawler = FileSystemCrawler()

        assert crawler._is_cad_file(Path("test.stl")) == True
        assert crawler._is_cad_file(Path("test.STL")) == True  # Case insensitive
        assert crawler._is_cad_file(Path("test.txt")) == False
        assert crawler._is_cad_file(Path("bracket.stl")) == True

    def test_discover_files_finds_stl_files(self):
        """Test that discover_files finds STL files in directory structure"""
        crawler = FileSystemCrawler()

        # Create temporary directory structure for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "bracket.stl").touch()
            (temp_path / "housing.stl").touch()
            (temp_path / "readme.txt").touch()  # Should be ignored

            # Create subdirectory with more files
            subdir = temp_path / "parts"
            subdir.mkdir()
            (subdir / "bolt.stl").touch()
            (subdir / "washer.stl").touch()

            # Discover files
            found_files = list(crawler.discover_files(str(temp_path)))
            found_names = [f.name for f in found_files]

            # Should find all STL files but not the txt file
            assert len(found_files) == 4
            assert "bracket.stl" in found_names
            assert "housing.stl" in found_names
            assert "bolt.stl" in found_names
            assert "washer.stl" in found_names
            assert "readme.txt" not in found_names

    def test_discover_files_empty_directory(self):
        """Test discover_files handles empty directories gracefully"""
        crawler = FileSystemCrawler()

        with tempfile.TemporaryDirectory() as temp_dir:
            found_files = list(crawler.discover_files(temp_dir))
            assert len(found_files) == 0

    def test_extract_project_info_from_directory_structure(self):
        """Test extracting project information from file paths"""
        crawler = FileSystemCrawler()

        # Test different directory structures
        file_path1 = Path("/projects/ProjectA/parts/bracket.stl")
        project1 = crawler.extract_project_info(file_path1, "/projects")
        assert project1 == "ProjectA"

        file_path2 = Path("/engineering/VehicleDesign/chassis/frame.stl")
        project2 = crawler.extract_project_info(file_path2, "/engineering")
        assert project2 == "VehicleDesign"

    def test_extract_project_info_handles_flat_structure(self):
        """Test project extraction when files are directly in root"""
        crawler = FileSystemCrawler()

        file_path = Path("/parts/bracket.stl")
        project = crawler.extract_project_info(file_path, "/parts")
        assert project == "Unknown"  # Should handle gracefully