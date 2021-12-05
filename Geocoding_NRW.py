# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoCodingNRW
                                 A QGIS plugin
 Geocoding test for NRW
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-12-04
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Cheick
        email                : cheick.cherif-haidara@stud.hs-bochum.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog,QMessageBox, QLineEdit
from qgis.core import QgsVectorLayer, QgsMapLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Geocoding_NRW_dialog import GeoCodingNRWDialog
import os.path


class GeoCodingNRW:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoCodingNRW_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GeoCodingNRW')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoCodingNRW', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Geocoding_NRW/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GoNRW'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True



    def select_output_file(self):
        filename, _filter = QFileDialog.getOpenFileName(
            self.dlg, "Select output file", "", "Shapefile (*.shp)")
        self.dlg.lineshp.setText(filename)
        if not filename or filename=='':
            return
        meinlayer=QgsVectorLayer(filename, "Mein Layer", "ogr")
        if not meinlayer or not meinlayer.isValid():
            QMessageBox.warning(self.iface.mainWindow(), "Sorry",
            "die Datei \"%s\" kann nicht geladen werden."% filename.replace('/',os.sep))
            return
        QgsProject.instance().addMapLayer(meinlayer)


   



   

    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GeoCodingNRW'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = GeoCodingNRWDialog()
        


            self.dlg.pushshp.clicked.connect(self.select_output_file)
       

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            layer = self.dlg.layerSelect.currentText()

            uri = self.plugin_dir+"/data/"+layer+".shp"

            nrw = self.iface.addVectorLayer(uri, "", "ogr")

            text_format = QgsTextFormat()

            text_format.setFont(QFont("Arial", 12))
            #text_format.setOrientation(QgsTextFormat.HorizontalOrientation) # ignored!?

            buffer_settings = QgsTextBufferSettings()
            buffer_settings.setEnabled(True)
            buffer_settings.setSize(1)
            buffer_settings.setColor(QColor("white"))

            text_format.setBuffer(buffer_settings)

            layer_settings  = QgsPalLayerSettings()

            layer_settings.fieldName = "GN"
            
            layer_settings.enabled = True
            layer_settings.setFormat(text_format)

            layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)

            nrw.setLabelsEnabled(True)
            nrw.setLabeling(layer_settings)


            nrw.triggerRepaint()
            # substitute with your code.
            pass
