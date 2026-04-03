# -*- coding: utf-8 -*-
"""
TiltMaster - RF Vertical Analysis for QGIS

Copyright (C) 2026 Achmad Amrulloh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

"""
launch_vertical_analysis.py

Entry action untuk menjalankan RF Vertical Analysis
dari QGIS toolbar.
"""

from qgis.core import QgsProject
from qgis.utils import iface

from ..modules.vertical_analysis.module import VerticalAnalysisModule


def launch_vertical_analysis():

    # ======================================================
    # FIND DEM LAYER - DENGAN FILTER LEBIH PINTAR
    # ======================================================

    dem_layer = None
    
    # Cari layer raster yang memiliki band elevation (bukan basemap)
    for lyr in QgsProject.instance().mapLayers().values():
        
        if lyr.type() == lyr.RasterLayer:
            layer_name = lyr.name().lower()
            
            # Skip basemap layers (biasanya mengandung kata tertentu)
            skip_keywords = ['bing', 'osm', 'openstreetmap', 'google', 'map', 'satellite', 'imagery', 'basemap']
            is_basemap = any(keyword in layer_name for keyword in skip_keywords)
            
            if not is_basemap:
                dem_layer = lyr
                print(f"✅ Found DEM layer: {lyr.name()}")
                break
    
    if dem_layer is None:
        # Fallback: ambil raster layer pertama yang bukan basemap
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.type() == lyr.RasterLayer:
                dem_layer = lyr
                print(f"⚠️ Using fallback raster layer: {lyr.name()}")
                break
    
    if dem_layer is None:
        iface.messageBar().pushCritical(
            "Vertical Analysis",
            "DEM layer not found in current project.\n\n"
            "Please load a DEM raster layer (e.g., SRTM, ASTER, or local DEM) "
            "before running analysis."
        )
        return

    # ======================================================
    # RUN MODULE
    # ======================================================

    try:

        module = VerticalAnalysisModule(
            dem_layer
        )

        module.run()

    except Exception as e:

        iface.messageBar().pushCritical(
            "Vertical Analysis",
            str(e)
        )