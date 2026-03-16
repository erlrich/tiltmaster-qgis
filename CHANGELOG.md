
## 📝 **Updated CHANGELOG.md**

```markdown
# Changelog

All notable changes to the TiltMaster plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-16

### Added
- Initial release of TiltMaster (formerly Tilting Tools)
- RF Vertical Analysis with terrain profiling using PyQtGraph
- Beam geometry calculation (main, upper, lower)
- Terrain intersection detection
- Coverage footprint generation
- Tilt Optimizer with 3 modes (Precise, Smart, Fast)
- Dual unit support (Metric/Imperial)
- Embedded map canvas with OSM basemap
- KMZ export for Google Earth
- CSV/Excel/JSON export for optimization results
- Online DEM source via Open-Meteo API
- LRU caching system for terrain data
- Comprehensive input validation
- User-friendly error messages
- About dialog with plugin information

### Changed
- Rebranded from "Tilting Tools" to "TiltMaster"
- Updated all UI text and menu entries
- New icon set for TiltMaster branding

### Features
- Draggable legends for map and profile views
- Real-time unit conversion
- Smart zoom to analysis area
- Reset view functionality
- Tooltips with RF engineering insights
- Progress tracking with time estimation
- Top 5 results with expandable details

### Dependencies
- **PyQtGraph** - Required for terrain profile visualization
- openpyxl (optional) - For Excel export
- xlsxwriter (optional) - Alternative Excel export

### Technical
- Centralized defaults in `defaults.py`
- Thread-safe optimization worker
- Memory management with closeEvent cleanup
- Consistent logging to console and QGIS message log
- Full English UI for international users
- Graceful handling of missing pyqtgraph with user-friendly error messages