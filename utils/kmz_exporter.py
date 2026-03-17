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
kmz_exporter.py

Export RF Analysis results to KMZ format for Google Earth
"""

import zipfile
import os
import tempfile
import math
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom

from qgis.core import QgsPointXY, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class KMZExporter:
    """
    Export RF sector and analysis to KMZ
    """
    
    def __init__(self, iface):
        self.iface = iface
    
    def export_sector(
        self,
        site_point,
        azimuth,
        h_beamwidth,
        footprint_start,
        footprint_end,
        impact_point=None,
        filename=None
    ):
        """
        Export sector to KMZ file
        """
        
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(
                self.iface.mainWindow(),
                "Save KMZ File",
                "",
                "KMZ Files (*.kmz)"
            )
            if not filename:
                return False
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                kml_path = os.path.join(tmpdir, "doc.kml")
                
                # Create KML content
                kml_content = self._generate_kml(
                    site_point,
                    azimuth,
                    h_beamwidth,
                    footprint_start,
                    footprint_end,
                    impact_point
                )
                
                # Write KML file
                with open(kml_path, 'w', encoding='utf-8') as f:
                    f.write(kml_content)
                
                # Create KMZ (ZIP)
                with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as kmz:
                    kmz.write(kml_path, "doc.kml")
                    
        except Exception as e:
            # Log error dengan detail
            print(f"❌ KMZ export failed: {e}")
            import traceback
            traceback.print_exc()
            raise
            
    
    def _generate_kml(
        self,
        site_point,
        azimuth,
        h_beamwidth,
        footprint_start,
        footprint_end,
        impact_point=None
    ):
        """
        Generate KML content
        """
        
        # Create KML root
        kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(kml, "Document")
        
        # Add styles
        self._add_styles(document)
        
        # Add site point
        self._add_site_point(document, site_point)
        
        # Add footprint polygon
        self._add_footprint(
            document,
            site_point,
            azimuth,
            h_beamwidth,
            footprint_start,
            footprint_end
        )
        
        # Add impact point
        if impact_point:
            self._add_impact_point(document, impact_point)
        
        # Add line of sight
        if impact_point:
            self._add_line_of_sight(document, site_point, impact_point)
        
        # Pretty print
        rough_string = ET.tostring(kml, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _add_styles(self, document):
        """Add KML styles"""
        
        # Site style
        site_style = ET.SubElement(document, "Style", id="siteStyle")
        site_icon = ET.SubElement(site_style, "IconStyle")
        ET.SubElement(site_icon, "color").text = "ff0000ff"  # Blue
        ET.SubElement(site_icon, "scale").text = "1.5"
        ET.SubElement(site_icon, "Icon").set("href", "http://maps.google.com/mapfiles/kml/shapes/triangle.png")
        
        # Impact style
        impact_style = ET.SubElement(document, "Style", id="impactStyle")
        impact_icon = ET.SubElement(impact_style, "IconStyle")
        ET.SubElement(impact_icon, "color").text = "ff0000ff"  # Red
        ET.SubElement(impact_icon, "scale").text = "1.2"
        ET.SubElement(impact_icon, "Icon").set("href", "http://maps.google.com/mapfiles/kml/shapes/target.png")
        
        # Footprint style
        footprint_style = ET.SubElement(document, "Style", id="footprintStyle")
        footprint_poly = ET.SubElement(footprint_style, "PolyStyle")
        ET.SubElement(footprint_poly, "color").text = "7f00ff00"  # Green transparent
        ET.SubElement(footprint_poly, "fill").text = "1"
        ET.SubElement(footprint_poly, "outline").text = "1"
        
        # Line style
        line_style = ET.SubElement(document, "Style", id="lineStyle")
        line_line = ET.SubElement(line_style, "LineStyle")
        ET.SubElement(line_line, "color").text = "ffff00ff"  # Yellow
        ET.SubElement(line_line, "width").text = "3"
    
    def _add_site_point(self, document, point):
        """Add site point placemark"""
        
        placemark = ET.SubElement(document, "Placemark")
        ET.SubElement(placemark, "name").text = "Site Location"
        ET.SubElement(placemark, "styleUrl").text = "#siteStyle"
        
        point_elem = ET.SubElement(placemark, "Point")
        ET.SubElement(point_elem, "coordinates").text = f"{point.x()},{point.y()},0"
    
    def _add_impact_point(self, document, point):
        """Add impact point placemark"""
        
        placemark = ET.SubElement(document, "Placemark")
        ET.SubElement(placemark, "name").text = "Impact Point"
        ET.SubElement(placemark, "styleUrl").text = "#impactStyle"
        
        point_elem = ET.SubElement(placemark, "Point")
        ET.SubElement(point_elem, "coordinates").text = f"{point.x()},{point.y()},0"
    
    def _add_footprint(self, document, center, azimuth, beamwidth, start_dist, end_dist):
        """Add footprint polygon"""
        
        # Generate polygon points
        points = self._generate_sector_polygon(
            center, azimuth, beamwidth, start_dist, end_dist
        )
        
        placemark = ET.SubElement(document, "Placemark")
        ET.SubElement(placemark, "name").text = "RF Footprint"
        ET.SubElement(placemark, "styleUrl").text = "#footprintStyle"
        
        polygon = ET.SubElement(placemark, "Polygon")
        outer = ET.SubElement(polygon, "outerBoundaryIs")
        linear_ring = ET.SubElement(outer, "LinearRing")
        
        coords_text = []
        for p in points:
            coords_text.append(f"{p.x()},{p.y()},0")
        
        ET.SubElement(linear_ring, "coordinates").text = " ".join(coords_text)
    
    def _add_line_of_sight(self, document, start, end):
        """Add line of sight"""
        
        placemark = ET.SubElement(document, "Placemark")
        ET.SubElement(placemark, "name").text = "Line of Sight"
        ET.SubElement(placemark, "styleUrl").text = "#lineStyle"
        
        line = ET.SubElement(placemark, "LineString")
        ET.SubElement(line, "coordinates").text = f"{start.x()},{start.y()},0 {end.x()},{end.y()},0"
    
    def _generate_sector_polygon(self, center, azimuth, beamwidth, start_dist, end_dist, steps=40):
        """Generate sector polygon points in WGS84"""
        
        start_angle = azimuth - beamwidth / 2
        end_angle = azimuth + beamwidth / 2
        
        R = 6378137.0
        lat1 = math.radians(center.y())
        lon1 = math.radians(center.x())
        
        points = []
        
        # Outer arc
        for i in range(steps + 1):
            angle_deg = start_angle + (end_angle - start_angle) * i / steps
            angle_rad = math.radians(angle_deg)
            
            lat2 = math.asin(
                math.sin(lat1) * math.cos(end_dist / R) +
                math.cos(lat1) * math.sin(end_dist / R) * math.cos(angle_rad)
            )
            lon2 = lon1 + math.atan2(
                math.sin(angle_rad) * math.sin(end_dist / R) * math.cos(lat1),
                math.cos(end_dist / R) - math.sin(lat1) * math.sin(lat2)
            )
            points.append(QgsPointXY(math.degrees(lon2), math.degrees(lat2)))
        
        # Inner arc (reverse)
        for i in range(steps, -1, -1):
            angle_deg = start_angle + (end_angle - start_angle) * i / steps
            angle_rad = math.radians(angle_deg)
            
            lat2 = math.asin(
                math.sin(lat1) * math.cos(start_dist / R) +
                math.cos(lat1) * math.sin(start_dist / R) * math.cos(angle_rad)
            )
            lon2 = lon1 + math.atan2(
                math.sin(angle_rad) * math.sin(start_dist / R) * math.cos(lat1),
                math.cos(start_dist / R) - math.sin(lat1) * math.sin(lat2)
            )
            points.append(QgsPointXY(math.degrees(lon2), math.degrees(lat2)))
        
        return points