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
