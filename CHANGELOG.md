# Changelog

All notable changes to the TiltMaster plugin will be documented in this file.

## [1.1.0] - 2026-04-03

### Added
- Navigation toolbar with Zoom In, Zoom Out, and Reset View buttons
- SVG icons for toolbar buttons and Export KMZ action
- KMZ compression (KML + PNG legend in single .kmz file)
- PNG legend support with proper positioning (top-left, 180px width)
- Dynamic plugin path detection for legend resources

### Fixed
- Zoom In/Out tools now work with single click (no drag required)
- Export KMZ now correctly handles user cancellation
- PyQtGraph error message now includes clickable link to troubleshooting guide
- Upper/Lower beam intersection points now correctly exported to KMZ
- Beam end point now uses 5000m hardcoded distance (matching plugin display)
- Sector polygon radius hardcoded to 5000m (matching plugin coverage map)
- Legend position corrected from bottom-left to top-left
- Memory leak with proper cache cleanup on dialog close

### Changed
- Legend HTML replaced with PNG image for better Google Earth compatibility
- KMZ export now includes embedded legend.png (no external dependencies)

## [1.0.0] - 2026-03-17

### Added
- RF Vertical Analysis with terrain profile visualization
- Beam geometry calculation (main, upper, lower beam angles)
- Terrain intersection detection and coverage footprint generation
- Tilt Optimizer with 3 modes (Precise, Smart, Fast)
- Dual unit support (Metric/Imperial) with real-time conversion
- Embedded map canvas with OSM basemap and layer selection
- Export results to KMZ (Google Earth), CSV, Excel, and JSON
- Online DEM source via Open-Meteo API (with offline fallback)
- About dialog with donation options (Buy Me a Coffee & Saweria)

### Fixed
- Memory leak in caching system
- QGIS not responding when closing after analysis
- Thread safety issues in terrain sampling
- Error handling for missing PyQtGraph dependency
- Coordinate validation with scientific notation support

### Dependencies
- **PyQtGraph** (>=0.13.0) - Required for terrain visualization

---

For detailed technical information, visit:
https://github.com/erlrich/tiltmaster-qgis