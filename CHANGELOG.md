# Changelog

All notable changes to the TiltMaster plugin will be documented in this file.

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