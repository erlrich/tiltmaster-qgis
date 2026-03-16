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
coverage_estimator.py

RF Coverage Estimator

Engine ini menentukan coverage distance final
berdasarkan beam geometry dan terrain intersection.

Coverage bisa disebabkan oleh:
1. Beam menyentuh ground
2. Beam terhalang terrain
"""

class CoverageEstimator:
    """
    Menghitung coverage distance final.
    """

    def __init__(self, antenna_height):
        self.antenna_height = antenna_height

    # ======================================================
    # SINGLE BEAM ESTIMATION
    # ======================================================

    def estimate(
        self,
        beam_distance,
        intersection_result
    ):
        """
        Estimate coverage distance untuk satu beam.

        Parameters
        ----------
        beam_distance : float
            jarak beam menyentuh ground

        intersection_result : dict
            hasil dari IntersectionSolver

        Returns
        -------
        dict
        """

        if intersection_result["blocked"]:

            return {
                "coverage_distance": intersection_result["distance"],
                "coverage_type": "terrain_blocked"
            }

        if beam_distance is None:

            return {
                "coverage_distance": None,
                "coverage_type": "no_ground_intersection"
            }

        return {
            "coverage_distance": beam_distance,
            "coverage_type": "ground_hit"
        }

    # ======================================================
    # MULTI BEAM ESTIMATION
    # ======================================================

    def estimate_all(
        self,
        beam_geometry,
        intersection_results
    ):
        """
        Estimate coverage untuk semua beam.

        Parameters
        ----------
        beam_geometry : dict
        intersection_results : dict

        Returns
        -------
        dict
        """

        upper = self.estimate(
            beam_geometry["distance_upper"],
            intersection_results["upper_beam"]
        )

        main = self.estimate(
            beam_geometry["distance_main"],
            intersection_results["main_beam"]
        )

        lower = self.estimate(
            beam_geometry["distance_lower"],
            intersection_results["lower_beam"]
        )

        return {
            "upper_beam": upper,
            "main_beam": main,
            "lower_beam": lower
        }

    # ======================================================
    # FINAL COVERAGE DISTANCE - FIXED (GUNAKAN INTERSECTION)
    # ======================================================

    def final_coverage(self, coverage_results):
        """
        Menentukan coverage final sektor.
        PRIORITY: main beam intersection > main beam free space
        """
        
        main = coverage_results["main_beam"]
        
        # PRIORITY 1: Main beam intersection
        if main["coverage_type"] in ["terrain_blocked", "ground_hit"]:
            if main["coverage_distance"] is not None:
                print(f"  ✅ Using main beam: {main['coverage_distance']:.0f}m ({main['coverage_type']})")
                return {
                    "distance": main["coverage_distance"],
                    "type": main["coverage_type"]
                }
        
        # PRIORITY 2: Main beam free space (hanya jika intersection None)
        if main["coverage_distance"] is not None:
            print(f"  ⚠️ No intersection, using free space: {main['coverage_distance']:.0f}m")
            return {
                "distance": main["coverage_distance"],
                "type": "ground_hit"
            }
        
        # Fallback ke lower beam
        lower = coverage_results["lower_beam"]
        return {
            "distance": lower["coverage_distance"],
            "type": lower["coverage_type"]
        }