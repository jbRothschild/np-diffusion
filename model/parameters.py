import numpy as  np
"""
Units: seconds, micrometers
"""
DIF_COEF = 0.05
VISC = 0.0
TOT_TIME = 3600. * .5 #30 minutes
TIME_STEP = .25
SAVE_TIME = 1800.
GLOB_DX = 2.
GLOB_DY = 2.
GLOB_DZ = 2.
LOAD_DIR = "../ChanLab/"
DOMAIN = "tissueboundary-cropped.tif"
VESSEL = "vesthresh-cropped.tif"
HOLES = "500000gaps.tif"
MPHAGE = "labelmac-cropped.tif"
NUCL = "labelnuc-cropped.tif"
GEN_HOLES = ""
