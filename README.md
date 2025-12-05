# CAD Redundancy Analyzer

A Python tool to analyze CAD file libraries and identify duplicate/similar components across projects, helping manufacturing companies reduce costs through component standardization.

## 🎯 Project Overview

Companies waste millions on duplicate parts and tooling because the same physical component exists under different part numbers across multiple projects. This tool automatically scans CAD file directories, analyzes geometric properties, and identifies duplicates—delivering measurable ROI through standardization.

## 🚧 Current Status

**Work in Progress** - Core functionality complete, report generation coming soon.

### Implemented Features

- ✅ **STL file discovery and scanning** - Recursive directory crawling with project detection
- ✅ **Geometric analysis** - Volume, surface area, bounding box extraction
- ✅ **Similarity detection algorithm** - Configurable threshold-based matching
- ✅ **Duplicate component identification** - Groups similar parts across projects
- ✅ **Test-driven development** - Comprehensive test suite with >90% coverage

### Planned Features

- [ ] HTML report generation with visualizations
- [ ] Excel/CSV export for easy sharing
- [ ] Command-line interface for engineers
- [ ] Support for additional CAD formats (STEP, IGES, SolidWorks)
- [ ] Web-based interface
- [ ] Continuous monitoring service
- [ ] Cost savings calculator

## 📋 Requirements

- Python 3.8+
- STL files exported from any CAD system

## 🚀 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/cad-redundancy-analyzer.git
cd cad-redundancy-analyzer

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage
```python
from cadRedundancyAnalyzer.core.analyzer import ComponentAnalyzer

# Initialize analyzer
analyzer = ComponentAnalyzer()

# Scan a directory of CAD files
analyzer.scan_directory("C:/Projects/CAD_Library")

# Find duplicates (95% similarity threshold)
duplicates = analyzer.find_duplicates(threshold=0.95)

# Display results
print(f"Found {len(duplicates)} duplicate groups")
for i, group in enumerate(duplicates, 1):
    print(f"\nGroup {i}: {len(group)} similar parts")
    for part in group:
        print(f"  - {part}")
```

### Advanced Usage
```python
from cadRedundancyAnalyzer.core.analyzer import ComponentAnalyzer
from cadRedundancyAnalyzer.discovery.filesystem import FileSystemCrawler

analyzer = ComponentAnalyzer()
crawler = FileSystemCrawler()

# Process files with custom logic
root_path = "C:/Engineering/Projects"
file_count = 0

for cad_file in crawler.discover_files(root_path):
    try:
        analyzer.process_file(str(cad_file), root_path)
        file_count += 1
        if file_count % 100 == 0:
            print(f"Processed {file_count} files...")
    except Exception as e:
        print(f"Error processing {cad_file}: {e}")

# Find duplicates with different thresholds
strict_duplicates = analyzer.find_duplicates(threshold=0.99)  # 99% match
loose_duplicates = analyzer.find_duplicates(threshold=0.90)   # 90% match

print(f"Strict duplicates: {len(strict_duplicates)} groups")
print(f"Loose duplicates: {len(loose_duplicates)} groups")
```

## 🧪 Testing

Run the full test suite:
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_analyzer.py -v

# Run with coverage report
pytest tests/ --cov=cadRedundancyAnalyzer --cov-report=html
```

## 📁 Project Structure
```
cad-redundancy-analyzer/
├── cadRedundancyAnalyzer/          # Main package
│   ├── core/                       # Core analysis logic
│   │   ├── models.py              # Data models (ComponentMetadata, GeometricSignature)
│   │   ├── analyzer.py            # Main ComponentAnalyzer class
│   │   └── similarity.py          # Similarity detection algorithms
│   ├── handlers/                   # CAD format handlers
│   │   ├── base.py                # Abstract base class for handlers
│   │   └── stl_handler.py         # STL file handler
│   └── discovery/                  # File discovery
│       └── filesystem.py          # Directory crawling and file discovery
├── tests/                          # Test suite
│   ├── test_model.py
│   ├── test_filesystem.py
│   ├── test_handler_stl.py
│   ├── test_similarity.py
│   └── test_analyzer.py
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                     # Git ignore patterns
```

## 🔧 How It Works

1. **File Discovery**: Recursively scans directories for CAD files (currently STL format)
2. **Geometric Analysis**: Extracts key properties from each file:
   - Volume (cm³)
   - Surface area (cm²)
   - Bounding box dimensions
   - Geometric hash (for quick comparison)
3. **Similarity Detection**: Compares all parts using weighted algorithm:
   - 50% weight on volume similarity
   - 30% weight on surface area similarity
   - 20% weight on bounding box dimensions
4. **Duplicate Grouping**: Groups parts that exceed similarity threshold (default 95%)

## 🎓 Development Philosophy

This project follows **Test-Driven Development (TDD)**:
- Tests written before implementation
- High test coverage (>90%)
- Continuous refactoring
- Incremental feature development

## 🗺️ Roadmap

### Phase 1: Core Functionality ✅ (Complete)
- [x] STL file parsing
- [x] Geometric property extraction
- [x] Similarity algorithm
- [x] Basic duplicate detection

### Phase 2: Usability (In Progress)
- [ ] HTML report generation
- [ ] Excel export functionality
- [ ] Command-line interface
- [ ] Progress indicators and logging

### Phase 3: Extended Format Support
- [ ] STEP file handler
- [ ] IGES file handler
- [ ] SolidWorks native format
- [ ] AutoCAD DWG/DXF

### Phase 4: Enterprise Features
- [ ] Web-based interface
- [ ] Database integration
- [ ] PLM system connectors (Windchill, Teamcenter)
- [ ] Continuous monitoring service
- [ ] Cost savings calculator and ROI reporting

## 🤝 Contributing

Contributions are welcome! This is an active project under development.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Implement your feature
5. Ensure all tests pass (`pytest tests/ -v`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow TDD: Write tests before implementation
- Maintain >90% test coverage
- Use type hints where appropriate
- Follow PEP 8 style guidelines
- Document new functions and classes

## 📄 License

MIT License

Copyright (c) 2025 Jack Tate

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 📧 Contact

Project Link: [https://github.com/yourusername/cad-redundancy-analyzer](https://github.com/jtatecc/cad-redundancy-analyzer)

## 🙏 Acknowledgments

- [numpy-stl](https://pypi.org/project/numpy-stl/) - STL file parsing
- [trimesh](https://github.com/mikedh/trimesh) - Mesh processing and geometric calculations
- [pytest](https://pytest.org/) - Testing framework

---

**Note**: This tool is designed to help identify potential duplicates. Always verify findings with engineering review before making part number consolidation decisions.
