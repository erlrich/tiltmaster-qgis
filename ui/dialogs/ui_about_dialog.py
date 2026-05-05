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

import os
import webbrowser

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'about_dialog_base.ui'))


class TiltMasterAboutDialog(QDialog, FORM_CLASS):
    """
    About dialog for TiltMaster - RF Vertical Analysis plugin
    Dengan opsi donasi Buy Me a Coffee (internasional) dan Saweria (Indonesia)
    """
    
    def __init__(self, parent=None):
        """Constructor."""
        super(TiltMasterAboutDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Connect donate button
        self.donateButton.clicked.connect(self._show_donation_options)
        
        # Set window title
        self.setWindowTitle("About TiltMaster")
    
    def _show_donation_options(self):
        """Show donation options dialog (improved UX)"""

        msg = QMessageBox(self)
        msg.setWindowTitle("Support TiltMaster")

        msg.setText(
            "If TiltMaster helps your RF optimization workflow\n"
            "(even saving a few minutes per task),\n\n"
            "you can support its development here:"
        )

        msg.setInformativeText(
            "Your support helps me continue building RF tools like this."
        )

        msg.setStandardButtons(QMessageBox.NoButton)

        # =====================================================
        # BUTTONS (with better hierarchy)
        # =====================================================
        bmac_btn = msg.addButton("☕ Support (International)", QMessageBox.AcceptRole)
        saweria_btn = msg.addButton("🇮🇩 Support (Indonesia)", QMessageBox.AcceptRole)
        cancel_btn = msg.addButton("Maybe later", QMessageBox.RejectRole)

        # Highlight primary button (BMAC)
        msg.setDefaultButton(bmac_btn)

        msg.exec_()

        if msg.clickedButton() == bmac_btn:
            QDesktopServices.openUrl(QUrl("https://buymeacoffee.com/achmad.amrulloh"))

        elif msg.clickedButton() == saweria_btn:
            QDesktopServices.openUrl(QUrl("https://saweria.co/achmadamrulloh"))