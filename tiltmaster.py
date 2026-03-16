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

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtCore import Qt
import os

from .actions.launch_vertical_analysis import launch_vertical_analysis
from .ui.dialogs.ui_about_dialog import TiltMasterAboutDialog


class TiltMaster:
    """
    Main plugin class for TiltMaster - RF Vertical Analysis
    """

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action_vertical_analysis = None
        self.action_about = None

    # ======================================================
    # INIT GUI
    # ======================================================

    def initGui(self):
        """
        Initialize plugin GUI - creates toolbar button and menu entry
        """
        # Icon path for RF Vertical Analysis
        vertical_icon_path = os.path.join(
            self.plugin_dir,
            'resources',
            'icons',
            'tiltmaster.svg'
        )

        # Create action for main analysis
        self.action_vertical_analysis = QAction(
            QIcon(vertical_icon_path),
            'TiltMaster - RF Vertical Analysis',
            self.iface.mainWindow()
        )

        # Connect signal
        self.action_vertical_analysis.triggered.connect(
            self.run_vertical_analysis
        )

        # Add to toolbar and menu
        self.iface.addToolBarIcon(self.action_vertical_analysis)
        self.iface.addPluginToMenu(
            'TiltMaster',
            self.action_vertical_analysis
        )
        
        # =====================================================
        # ABOUT DIALOG
        # =====================================================
        # Icon path for About dialog
        about_icon_path = os.path.join(
            self.plugin_dir,
            'resources',
            'icons',
            'information.svg'
        )
        
        # Create about action with icon
        self.action_about = QAction(
            QIcon(about_icon_path),
            'About TiltMaster',
            self.iface.mainWindow()
        )
        
        self.action_about.triggered.connect(self.show_about_dialog)
        
        # Add to menu only (not toolbar)
        self.iface.addPluginToMenu(
            'TiltMaster',
            self.action_about
        )

    # ======================================================
    # UNLOAD
    # ======================================================

    def unload(self):
        """
        Clean up when plugin is unloaded
        """
        if self.action_vertical_analysis:
            self.iface.removeToolBarIcon(self.action_vertical_analysis)
            self.iface.removePluginMenu(
                'TiltMaster', 
                self.action_vertical_analysis
            )
            self.action_vertical_analysis = None
            
        if self.action_about:
            self.iface.removePluginMenu(
                'TiltMaster',
                self.action_about
            )
            self.action_about = None

    # ======================================================
    # ACTIONS
    # ======================================================

    def run_vertical_analysis(self):
        """
        Launch RF Vertical Analysis dialog
        """
        try:
            launch_vertical_analysis()
        except Exception as e:
            QMessageBox.critical(
                None,
                "TiltMaster Error",
                f"An error occurred while launching TiltMaster:\n\n{str(e)}"
            )
            # Re-raise for debugging
            raise
            
    def show_about_dialog(self):
        """
        Show about dialog with proper window management
        """
        print("\n" + "="*60)
        print("🔍 MENU CLICK DETECTED!")
        print("="*60)
        
        try:
            from .ui.dialogs.ui_about_dialog import TiltMasterAboutDialog
            print("✅ Import successful")
            
            # Buat dialog tanpa parent agar independen
            dlg = TiltMasterAboutDialog()
            print("✅ Dialog created")
            
            # Set flags untuk memastikan dialog muncul di atas
            dlg.setWindowFlags(
                Qt.Window | 
                Qt.WindowStaysOnTopHint | 
                Qt.WindowCloseButtonHint
            )
            
            # Paksa di atas
            dlg.raise_()
            dlg.activateWindow()
            
            print("🎬 Executing dialog...")
            dlg.exec_()
            print("✅ Dialog closed")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()