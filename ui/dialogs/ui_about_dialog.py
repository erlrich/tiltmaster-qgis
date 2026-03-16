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

from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtCore import Qt


class TiltMasterAboutDialog(QDialog):
    """
    About dialog for TiltMaster - RF Vertical Analysis plugin
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About TiltMaster")
        self.setFixedWidth(460)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("TiltMaster")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0c6075; margin-bottom: 4px;")

        # Subtitle
        subtitle = QLabel("RF Vertical Analysis for QGIS")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #2c5a6b; font-size: 12px; margin-bottom: 8px;")

        # Version
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #5f7a84; font-size: 11px; font-weight: bold; margin-bottom: 12px;")

        # Description
        description = QLabel(
            "Advanced RF planning tools for telecommunication engineers.\n\n"
            "Features:\n"
            "• Vertical beam analysis with terrain profiling\n"
            "• Beam intersection detection and coverage footprint\n"
            "• Tilt optimizer with 3 optimization modes\n"
            "• Dual unit support (Metric/Imperial)\n"
            "• Embedded map canvas with OSM basemap\n"
            "• KMZ export for Google Earth\n"
            "• Results export to CSV, Excel, and JSON"
        )
        description.setAlignment(Qt.AlignLeft)
        description.setWordWrap(True)
        description.setStyleSheet("margin-top: 10px; margin-bottom: 10px; line-height: 1.4;")

        # Separator line
        separator = QLabel("")
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #c9d9e0; margin: 8px 0;")

        # Author info
        author = QLabel(
            "Author  : Achmad Amrulloh\n"
            "Email   : achmad.amrulloh@gmail.com\n"
            "LinkedIn: https://www.linkedin.com/in/achmad-amrulloh/\n"
            "GitHub  : https://github.com/erlrich/tiltmaster-qgis"
        )
        author.setAlignment(Qt.AlignLeft)
        author.setStyleSheet("color: #2c5a6b; font-size: 10px; margin-top: 5px;")
        author.setOpenExternalLinks(True)

        # License
        license_text = QLabel(
            "© 2026 Achmad Amrulloh\n\n"
            "This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.\n\n"
            "This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details.\n\n"
            "You should have received a copy of the GNU General Public License "
            "along with this program. If not, see <https://www.gnu.org/licenses/>."
        )
        license_text.setAlignment(Qt.AlignCenter)
        license_text.setWordWrap(True)
        license_text.setStyleSheet("color: #5f7a84; font-size: 9px; margin-top: 10px;")

        # OK Button
        btn = QPushButton("OK")
        btn.setFixedWidth(100)
        btn.setMinimumHeight(30)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0c6075;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #094e60;
            }
        """)
        btn.clicked.connect(self.accept)

        # Add all widgets to layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addWidget(separator)
        layout.addWidget(author)
        layout.addWidget(license_text)
        layout.addStretch()
        layout.addWidget(btn, 0, Qt.AlignCenter)