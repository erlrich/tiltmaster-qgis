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

from qgis.PyQt.QtGui import QIcon, QPixmap, QColor, QPainter, QFont
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QSplashScreen
from qgis.PyQt.QtCore import Qt, QTimer
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
        self.splash = None
        self._dialog_launched = False
        
    
    def _check_dependencies(self):
        """
        Check required Python dependencies (non-blocking)
        """
        if hasattr(self, "_dependency_checked"):
            return True

        self._dependency_checked = True

        try:
            from defusedxml.minidom import parseString  # noqa: F401
            print("✅ defusedxml available")
            return True
        except ImportError:
            print("⚠️ defusedxml not installed")

            msg = QMessageBox(self.iface.mainWindow())
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("TiltMaster - Optional Dependency")
            msg.setText("Optional dependency 'defusedxml' is not installed.")
            msg.setInformativeText(
                "KMZ export will still work, but without enhanced security.\n\n"
                "Recommended installation:\n"
                "python -m pip install --user \"defusedxml>=0.7.1\""
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

            return False
    
    # def _check_dependencies(self):
        # QMessageBox.information(self.iface.mainWindow(), "DEBUG", "Dependency check triggered")
        # if hasattr(self, "_dependency_checked"):
            # return True

        # self._dependency_checked = True

        # try:
            # raise ImportError("Simulated missing module")  # <-- TEST MODE
        # except ImportError:
            # msg = QMessageBox(self.iface.mainWindow())
            # msg.setIcon(QMessageBox.Warning)
            # msg.setWindowTitle("TiltMaster - Optional Dependency")
            # msg.setText("Optional dependency 'defusedxml' is not installed.")
            # msg.exec_()
            # return False
        
    # ======================================================
    # INIT GUI
    # ======================================================

    def initGui(self):
        """
        Initialize plugin GUI - creates toolbar button and menu entry
        """
        
        # Check optional dependencies (non-blocking)
        self._check_dependencies()
        
        vertical_icon_path = os.path.join(
            self.plugin_dir,
            'resources',
            'icons',
            'tiltmaster.png'
        )

        self.action_vertical_analysis = QAction(
            QIcon(vertical_icon_path),
            'TiltMaster - RF Vertical Analysis',
            self.iface.mainWindow()
        )
        
        self.action_vertical_analysis.setToolTip(
            "TiltMaster - RF Vertical Analysis\n"
            "Click to open analysis dialog\n"
            "☕ Support: buymeacoffee.com/achmad.amrulloh"
        )
        
        self.action_vertical_analysis.setStatusTip(
            "TiltMaster - RF Vertical Analysis | Support: buymeacoffee.com/achmad.amrulloh"
        )
        
        self.action_vertical_analysis.triggered.connect(
            self.run_vertical_analysis
        )

        self.iface.addToolBarIcon(self.action_vertical_analysis)
        self.iface.addPluginToMenu(
            'TiltMaster',
            self.action_vertical_analysis
        )
        
        # ABOUT DIALOG
        about_icon_path = os.path.join(
            self.plugin_dir,
            'resources',
            'icons',
            'information.png'
        )
        
        self.action_about = QAction(
            QIcon(about_icon_path),
            'About TiltMaster',
            self.iface.mainWindow()
        )
        
        self.action_about.triggered.connect(self.show_about_dialog)
        
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
    # SPLASH SCREEN METHODS
    # ======================================================  
       
    def _create_splash_pixmap(self, message="Loading RF Engine..."):
        """
        Create splash screen pixmap with TiltMaster branding
        
        Parameters
        ----------
        message : str
            Message to display on splash screen
        """
        width = 420
        height = 220
        
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#0c6075"))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # =====================================================
        # TITLE (sedikit lebih ke atas)
        # =====================================================
        title_font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(
            pixmap.rect().adjusted(0, 10, 0, -140),
            Qt.AlignCenter,
            "TiltMaster"
        )

        # =====================================================
        # SUBTITLE (rapat dengan title)
        # =====================================================
        subtitle_font = QFont("Arial", 11, QFont.Bold)
        painter.setFont(subtitle_font)
        painter.setPen(QColor(200, 200, 200))
        painter.drawText(
            pixmap.rect().adjusted(0, 40, 0, -120),
            Qt.AlignCenter,
            "RF Vertical Analysis for QGIS"
        )

        # =====================================================
        # MESSAGE (tengah - jadi anchor utama)
        # =====================================================
        message_font = QFont("Arial", 10)
        painter.setFont(message_font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(
            pixmap.rect().adjusted(0, 85, 0, -80),
            Qt.AlignCenter,
            message
        )

        # =====================================================
        # LOADING DOTS (dekat message)
        # =====================================================
        loading_font = QFont("Arial", 10)
        painter.setFont(loading_font)
        painter.setPen(QColor(100, 200, 255))
        painter.drawText(
            pixmap.rect().adjusted(0, 110, 0, -60),
            Qt.AlignCenter,
            "● ● ● ● ●"
        )

        # =====================================================
        # SUPPORT MESSAGE (dipisah lebih bawah, tidak padat)
        # =====================================================
        footer_font = QFont("Arial", 10)
        painter.setFont(footer_font)

        # Line 1 (lebih soft)
        painter.setPen(QColor(170, 210, 220))
        painter.drawText(
            pixmap.rect().adjusted(0, 150, 0, -10),
            Qt.AlignCenter,
            "If this saves your RF optimization time…"
        )

        # Line 2 (highlight ringan)
        footer_font_bold = QFont("Arial", 11, QFont.Bold)
        painter.setFont(footer_font_bold)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(
            pixmap.rect().adjusted(0, 170, 0, 10),
            Qt.AlignCenter,
            "☕ Support TiltMaster"
        )
        
        # =====================================================
        # HAPUS FOOTER DONASI DARI SPLASH SCREEN
        # (Pindahkan ke status bar atau tempat lain)
        # =====================================================
        # Footer sudah dihapus - tidak perlu ditampilkan di splash
        
        painter.end()
        
        return pixmap
    
    def _show_splash_with_progress(self):
        """
        Show splash screen with animated progress messages
        (Improved: last frame hold for better visual impact)
        """
        self._dialog_launched = False

        # =====================================================
        # SEMBUNYIKAN TOOLTIP SEMENTARA
        # =====================================================
        original_tooltip = ""
        if self.action_vertical_analysis:
            original_tooltip = self.action_vertical_analysis.toolTip()
            self.action_vertical_analysis.setToolTip("")

        # Buat splash screen
        splash_pixmap = self._create_splash_pixmap("Initializing...")
        self.splash = QSplashScreen(self.iface.mainWindow(), splash_pixmap)

        self.splash.setWindowFlags(
            Qt.SplashScreen | 
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )

        self.splash.setToolTip("")
        self.splash.setMouseTracking(False)
        self.splash.setEnabled(False)
        self.splash.show()

        # Center screen
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_geom = screen.availableGeometry()
            splash_geom = self.splash.geometry()
            x = (screen_geom.width() - splash_geom.width()) // 2
            y = (screen_geom.height() - splash_geom.height()) // 2
            self.splash.move(x, y)

        # =====================================================
        # LOADING MESSAGES
        # =====================================================
        loading_messages = [
            "Loading RF Engine...",
            "Initializing Terrain Sampler...",
            "Preparing Analysis Tools...",
            "Almost ready...",
            "Launching TiltMaster..."
        ]

        # =====================================================
        # TIMING CONFIG (KEY IMPROVEMENT)
        # =====================================================
        normal_delay = 300   # cepat untuk animasi awal
        final_delay = 1200    # tahan lebih lama di frame terakhir

        def update_splash_message(index=0):
            if not self.splash or not self.splash.isVisible():
                return

            # Update message
            new_pixmap = self._create_splash_pixmap(loading_messages[index])
            self.splash.setPixmap(new_pixmap)

            # Kalau bukan terakhir → lanjut cepat
            if index < len(loading_messages) - 1:
                QTimer.singleShot(normal_delay, lambda: update_splash_message(index + 1))
            else:
                # =====================================================
                # LAST FRAME HOLD (KEY PART)
                # =====================================================
                QTimer.singleShot(final_delay, lambda: self._open_dialog_after_splash(original_tooltip))

        # Start animation
        update_splash_message(0)
    
    def _open_dialog_after_splash(self, original_tooltip=""):
        """
        Close splash screen and open the actual dialog
        """
        # KEMBALIKAN TOOLTIP
        if self.action_vertical_analysis and original_tooltip:
            self.action_vertical_analysis.setToolTip(original_tooltip)
        
        if self._dialog_launched:
            print("⚠️ Dialog already launched, skipping...")
            return
        
        if self.splash:
            try:
                self.splash.close()
                self.splash = None
            except:
                pass
        
        self._dialog_launched = True
        self._launch_dialog()
    
    def _launch_dialog(self):
        """
        Actual method to launch the vertical analysis dialog
        """
        try:
            from qgis.core import QgsProject
            from qgis.utils import iface
            from .modules.vertical_analysis.module import VerticalAnalysisModule
            
            # Cari DEM layer
            dem_layer = None
            
            for lyr in QgsProject.instance().mapLayers().values():
                if lyr.type() == lyr.RasterLayer:
                    layer_name = lyr.name().lower()
                    skip_keywords = ['bing', 'osm', 'openstreetmap', 'google', 'map', 'satellite', 'imagery', 'basemap']
                    is_basemap = any(keyword in layer_name for keyword in skip_keywords)
                    
                    if not is_basemap:
                        dem_layer = lyr
                        print(f"✅ Found DEM layer: {lyr.name()}")
                        break
            
            if dem_layer is None:
                for lyr in QgsProject.instance().mapLayers().values():
                    if lyr.type() == lyr.RasterLayer:
                        dem_layer = lyr
                        print(f"⚠️ Using fallback raster layer: {lyr.name()}")
                        break
            
            if dem_layer is None:
                iface.messageBar().pushCritical(
                    "Vertical Analysis",
                    "DEM layer not found in current project.\n\n"
                    "Please load a DEM raster layer before running analysis."
                )
                return
            
            module = VerticalAnalysisModule(dem_layer)
            module.run()
            
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "TiltMaster Error",
                f"An error occurred while launching TiltMaster:\n\n{str(e)}"
            )
            raise

    # ======================================================
    # ACTIONS
    # ======================================================

    def run_vertical_analysis(self):
        """
        Launch RF Vertical Analysis dialog with splash screen animation
        """
        print("\n" + "="*60)
        print("🚀 TiltMaster - Launching with Splash Screen")
        print("="*60)
        
        self._dialog_launched = False
        self._show_splash_with_progress()
            
    def show_about_dialog(self):
        """
        Show about dialog with proper window management
        """
        print("\n" + "="*60)
        print("🔍 MENU CLICK DETECTED!")
        print("="*60)
        
        try:
            from .ui.dialogs.ui_about_dialog import TiltMasterAboutDialog
            
            dlg = TiltMasterAboutDialog()
            
            dlg.setWindowFlags(
                Qt.Window | 
                Qt.WindowStaysOnTopHint | 
                Qt.WindowCloseButtonHint
            )
            
            dlg.raise_()
            dlg.activateWindow()
            
            dlg.exec_()
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()