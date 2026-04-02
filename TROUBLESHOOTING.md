# TiltMaster - Troubleshooting Guide

## PyQtGraph Not Installed

### Symptoms
- Terrain profile widget shows error message
- "PyQtGraph Not Installed" appears in the analysis dialog
- Error: `No module named 'pyqtgraph'`

### Solution

Choose one of the following methods:

---

#### Option 1: Install via OSGeo4W (Recommended for Windows)

1. **Open OSGeo4W Shell**
   - Click Start Menu
   - Search for "OSGeo4W Shell"
   - Run as Administrator (right-click → Run as administrator)

2. **Run installation command**
osgeo4w-setup -k pyqtgraph

text

3. **Follow the setup wizard**
- Select "Install" or "Upgrade"
- Choose the pyqtgraph package
- Complete the installation

4. **Restart QGIS**

> 💡 **Screenshot Reference:**
> ![OSGeo4W Shell](docs/images/osgeo4w_shell.png)
> *OSGeo4W Shell interface after running the command*

---

#### Option 2: Install via QGIS Python Console

1. Open QGIS Python Console
- `Plugins → Python Console` or press `Ctrl+Alt+P`

2. Run the following command:
```python
import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqtgraph'])
Restart QGIS

Option 3: Using pip in OSGeo4W Shell
Open OSGeo4W Shell and run:

bash
python -m pip install pyqtgraph
Option 4: Manual Download
Download pyqtgraph from: https://pypi.org/project/pyqtgraph/

Extract the package

Copy to QGIS Python site-packages folder:

Typical location: C:\OSGeo4W\apps\Python39\Lib\site-packages\

Verification
After installation, verify PyQtGraph is installed:

Open QGIS Python Console

Run:

python
import pyqtgraph
print(pyqtgraph.__version__)
If version number appears, installation was successful.

Common Issues
"pip is not recognized"
Solution: Use OSGeo4W Shell instead of regular Command Prompt.

"Access denied" error
Solution: Run OSGeo4W Shell as Administrator.

Package already installed but still error
Solution:

Check if multiple Python versions exist

Restart QGIS completely (not just the plugin)

Try reinstalling with --force-reinstall flag

Other Common Issues
DEM Layer Not Found
Symptom: "No DEM layer found in current project"

Solution:

Load a DEM raster layer (e.g., SRTM, ASTER) into your QGIS project

Ensure the layer is a valid raster layer

Try switching to "Open-Meteo (Online)" source if no local DEM is available

Basemap Not Loading
Symptom: Map is blank or white

Solution:

Check your internet connection

Try selecting a different basemap from the dropdown

Click the refresh button (↻) to reload basemap list

Export to KMZ Fails
Symptom: "KMZ export failed" message

Solution:

Ensure you have write permissions to the destination folder

Try saving to a different location (e.g., Desktop)

Check if the filename contains special characters

No Elevation Data (All terrain = 0)
Symptom: Terrain profile shows flat line at 0m elevation

Solution:

Local DEM: Ensure you have loaded a valid DEM raster layer

Online Source: Check your internet connection

Verify the site coordinates are within DEM coverage area

Getting Help
If you continue to experience issues:

Check QGIS Log Messages

View → Panels → Log Messages

Look for "TiltMaster" in the log

Report on GitHub

Include: OS version, QGIS version, and error messages

Attach screenshot if possible

Repository: https://github.com/erlrich/tiltmaster-qgis

Support Development
If TiltMaster helps your work, consider supporting its development:

🌐 International: https://buymeacoffee.com/achmad.amrulloh

🇮🇩 Indonesia: https://saweria.co/achmadamrulloh

Last updated: April 2026