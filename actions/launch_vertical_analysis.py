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
    # FIND DEM LAYER
    # ======================================================

    dem_layer = None

    for lyr in QgsProject.instance().mapLayers().values():

        if lyr.type() == lyr.RasterLayer:

            dem_layer = lyr
            break

    if dem_layer is None:

        iface.messageBar().pushCritical(
            "Vertical Analysis",
            "DEM layer not found in current project."
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