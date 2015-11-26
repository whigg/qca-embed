#!/usr/bin/env python

# -----------------------------------
# Name: application.py
# Desc: Main loop for QCA embedder application
# Author: Jake Retallick
# Created: 2015.11.25
# Modified: 2015.11.25
# Licence: Copyright 2015
# -----------------------------------

from PyQt4 import QtGui

# MAIN WINDOW SETTINGS
WIN_DX = 1000   # width of the main window
WIN_DY = 600    # height of the main window
WIN_X0 = 100    # x-offset of the main window
WIN_Y0 = 100    # y-offset of the main window

ICO_SIZE = 30           # icon size
ICO_DIR = '/gui/ico/'   # icon directory

BUTTON_SIZE = 25    # size of buttons

# QCA CELL PARAMETERS
CELL_SEP = 50
CELL_SIZE = 1.*CELL_SEP
CELL_ALPHA = int(.15*255)

# --colors
QCA_COL = {'default': QtGui.QColor(255, 255, 255),
           'inactive': QtGui.QColor(100, 100, 100),
           'output': QtGui.QColor(0, 200, 0, 150),
           'input': QtGui.QColor(200, 0, 0, 150),
           'fixed': QtGui.QColor(255, 165, 0, 150)}

DOT_RAD = 0.25*CELL_SIZE

# --qca pen
CELL_PEN_WIDTH = max(1, int(0.05*CELL_SIZE))
CELL_PEN_COLOR = QtGui.QColor(180, 180, 180)
TEXT_PEN_WIDTH = max(1, int(0.05*CELL_SIZE))
TEXT_PEN_COLOR = QtGui.QColor(0, 0, 0)

# --qca magnification
MAX_MAG = 5
MIN_MAG = 0.1
MAG_STEP = 0.1