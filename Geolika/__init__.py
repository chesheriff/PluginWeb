# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoLika
                                 A QGIS plugin
 Geocoding für Liegenschaft
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-12-09
        copyright            : (C) 2021 by Cheick
        email                : cheick.cherif-haidara@stud.hs-bochum.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeoLika class from file GeoLika.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GeoLika import GeoLika
    return GeoLika(iface)

    
