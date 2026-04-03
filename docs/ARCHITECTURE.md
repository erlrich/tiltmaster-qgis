# TiltMaster Architecture Guide

## 📋 Overview

TiltMaster is a QGIS plugin for RF Vertical Analysis, designed for telecommunication engineers to perform vertical beam analysis, terrain intersection detection, coverage footprint calculation, and tilt optimization.
Current version: **1.1.0** (2026-04-03)

## 🏗️ Project Structure
TiltMaster/
│
├── init.py # Plugin entry point
├── metadata.txt # Plugin metadata for QGIS
├── tiltmaster.py # Main plugin class
│
├── actions/ # Plugin actions (toolbar/menu)
│ ├── init.py
│ └── launch_vertical_analysis.py
│
├── core/ # Core business logic
│ ├── init.py
│ │
│ ├── terrain/ # Terrain processing
│ │ ├── init.py
│ │ ├── terrain_sampler.py # DEM sampling (local/online)
│ │ └── terrain_profile.py # Terrain profile calculations
│ │
│ ├── rf_engine/ # RF calculations
│ │ ├── init.py
│ │ ├── beam_geometry.py # Vertical beam geometry
│ │ ├── intersection_solver.py # Beam-terrain intersection
│ │ ├── coverage_estimator.py # Coverage distance estimation
│ │ └── vertical_analysis_engine.py # Main orchestrator
│ │
│ └── models/ # Data models
│ ├── init.py
│ └── rf_result.py # RF analysis result model
│
├── infrastructure/ # Infrastructure components
│ ├── init.py
│ │
│ ├── layers/ # Layer management
│ │ ├── init.py
│ │ └── layer_manager.py # QGIS layer lifecycle
│ │
│ ├── rendering/ # Map rendering
│ │ ├── init.py
│ │ └── map_renderer.py # Render results to map
│ │
│ └── geometry/ # Geometry utilities
│ ├── init.py
│ └── sector_geometry.py # Sector polygon generation
│
├── modules/ # Feature modules
│ └── vertical_analysis/ # Vertical analysis module
│ ├── init.py
│ ├── controller.py # UI-Engine bridge
│ ├── map_engine.py # Map rendering for module
│ ├── module.py # Module entry point
│ │
│ └── utils/ # Module-specific utilities
│ ├── init.py
│ └── sector_builder.py # Sector polygon builder
│
├── ui/ # User Interface
│ ├── init.py
│ │
│ ├── dialogs/ # Dialog windows
│ │ ├── init.py
│ │ ├── defaults.py # Default RF parameters
│ │ ├── ui_about_dialog.py # About dialog
│ │ └── vertical_analysis_dialog.py # Main analysis dialog
│ │
│ └── widgets/ # Reusable widgets
│ ├── init.py
│ ├── map_legend_frame.py # Map legend overlay
│ ├── profile_legend_frame.py # Profile legend overlay
│ ├── sector_map_widget.py # Embedded map canvas
│ └── terrain_profile_widget.py # Terrain profile graph
│
├── utils/ # General utilities
│ ├── init.py
│ ├── kmz_exporter.py # KMZ export functionality
│ └── logging_utils.py # Logging utilities
│
├── resources/ # Static resources
│   ├── legend/
│   │   └── legend.png          # PNG legend untuk KMZ export
│   │
│ 	└── icons/
│	 	├── tower.svg # Tower icon for profile
│       ├── information.png     # Icon untuk About dialog
│       ├── zoom-in.svg         # Navigation toolbar icons
│       ├── zoom-out.svg
│       ├── reset-view.svg
│	 	└── vertical_visual.png # Plugin icon
│
└── docs/ # Documentation
└── ARCHITECTURE.md # This file



## 🔄 Data Flow

### 1. **User Interaction Flow**
User clicks toolbar button
→ actions/launch_vertical_analysis.py
→ Finds DEM layer in project
→ modules/vertical_analysis/module.py
→ Creates controller & opens dialog
→ ui/dialogs/vertical_analysis_dialog.py



### 2. **Analysis Flow (Run Analysis)**
Dialog collects parameters
→ modules/vertical_analysis/controller.py
→ core/rf_engine/vertical_analysis_engine.py
→ core/terrain/terrain_sampler.py (sample DEM)
→ core/terrain/terrain_profile.py (calculate angles)
→ core/rf_engine/beam_geometry.py (calculate beams)
→ core/rf_engine/intersection_solver.py (find intersections)
→ core/rf_engine/coverage_estimator.py (final coverage)



### 3. **Visualization Flow**
Analysis results returned to controller
→ ui/dialogs/vertical_analysis_dialog.py
→ ui/widgets/terrain_profile_widget.py (update graph)
→ ui/widgets/sector_map_widget.py (update map)
→ infrastructure/layers/layer_manager.py (manage layers)
→ modules/vertical_analysis/utils/sector_builder.py (build polygons)



### 4. **Optimization Flow**
User starts optimization in dialog
→ Background thread with OptimizeWorker
→ Iterates through tilt combinations
→ Uses cached results for speed
→ Calls controller.run_analysis() for new combos
→ Returns top 5 results
→ Updates UI with progress & results



### 5. **KMZ Export Flow**
User clicks Export KMZ button
→ utils/kmz_exporter.py
→ Checks for legend.png in resources/legend/
→ Generates KML with ScreenOverlay (PNG legend)
→ Creates temporary folder
→ Compresses KML + legend.png into .kmz (ZIP)
→ Cleans up temporary files
→ Opens save dialog



## 🧩 Key Components

### Core Engine (`core/`)
- **TerrainSampler**: Samples elevation data from local DEM or Open-Meteo API
- **TerrainProfile**: Calculates terrain angles relative to antenna
- **BeamGeometry**: Computes main/upper/lower beam angles
- **IntersectionSolver**: Finds where beams intersect terrain
- **CoverageEstimator**: Determines final coverage distance
- **VerticalAnalysisEngine**: Orchestrates the entire analysis pipeline

### Infrastructure (`infrastructure/`)
- **LayerManager**: Manages QGIS layer lifecycle (create/get/clear)
- **MapRenderer**: Renders results to main QGIS canvas
- **SectorGeometry**: Creates sector polygons for visualization

### UI Components (`ui/`)
- **VerticalAnalysisDialog**: Main dialog with RF parameters
- **TerrainProfileWidget**: PyQtGraph-based terrain profile visualization
- **SectorMapWidget**: Embedded QGIS map canvas with RF layers
- **Legend Frames**: Draggable legend overlays for map and profile

### Utilities (`utils/`)
- **KMZExporter**: Exports analysis results to Google Earth KMZ format
  - PNG legend overlay (top-left, 180px width)
  - Sector polygon with 5000m hardcoded radius
  - Upper/Lower beam intersection points
  - Beam end point at 5000m
  - KMZ compression (ZIP with embedded PNG)

## 📊 Class Relationships
VerticalAnalysisModule
└── VerticalAnalysisController
├── VerticalAnalysisEngine
│ ├── TerrainSampler
│ ├── TerrainProfile
│ ├── BeamGeometry
│ ├── IntersectionSolver
│ └── CoverageEstimator
└── VerticalAnalysisMapEngine
└── LayerManager

VerticalAnalysisDialog
├── TerrainProfileWidget
│ └── ProfileLegendFrame
├── SectorMapWidget
│ ├── LayerManager
│ ├── MapLegendFrame
│ └── (embedded QgsMapCanvas)
└── OptimizeWorker (background thread)



## 🔧 Configuration

Default parameters are centralized in `ui/dialogs/defaults.py`:

```python
class RFDefaults:
    ANTENNA_HEIGHT = 40          # meters
    MECHANICAL_TILT = 4          # degrees
    ELECTRICAL_TILT = 2          # degrees
    VERTICAL_BEAMWIDTH = 6       # degrees
    HORIZONTAL_BEAMWIDTH = 65    # degrees
    MAX_DISTANCE = 3000          # meters
    SAMPLING_STEP = 30           # meters
    # ... more defaults

## 🖼️ Resources

### Legend PNG
- Location: `resources/legend/legend.png`
- Size: 400x360 pixels (HD)
- Format: PNG with transparency
- Used for: KMZ export ScreenOverlay
- Generated once via script or manually
	
🌐 External Dependencies
- QGIS: Core GIS functionality
- PyQt5: UI framework
- PyQtGraph: Fast scientific plotting
- Open-Meteo API: Online elevation data (optional)
- openpyxl: Excel export (optional)

🚀 Performance Optimizations
- Terrain Caching: Results cached with LRU strategy
- Optimization Cache: Results stored during optimization runs
- Binary Search: Fast mouse-over in profile widget
- Threading: Optimization runs in background thread
- Garbage Collection: Periodic cleanup during long operations

🔌 Extension Points
- The plugin is designed to be extensible:
- New Data Sources: Add new DEM providers in terrain_sampler.py
- Additional Analyses: Create new modules in modules/
- Custom Visualizations: Extend widgets in ui/widgets/
- Export Formats: Add new exporters in utils/

📝 Development Guidelines
- Import Conventions
- Use relative imports within the plugin
- Absolute imports only for external libraries
- Error Handling
- Validate inputs before processing
- Provide user-friendly error messages
- Log errors to QGIS message log

UI Design
- Consistent color scheme (#0c6075 primary)
- Responsive layouts with scroll areas
- Draggable overlays for legends
- Dual unit support (Metric/Imperial)

Threading
- UI never blocks
- Optimization runs in background
- Proper cleanup of threads in closeEvent

📄 License
- MIT License - See LICENSE file for details