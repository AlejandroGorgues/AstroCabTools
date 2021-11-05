    #-*- coding: utf-8 -*-

"""
Method that read the galaxy lines from an ascii file
"""

import numpy as np
import pandas as pd

import sys
import io

from astropy.io import fits
from jwst import datamodels

__all__ = ['get_galaxy_lines']

def get_galaxy_lines(path):
    df = pd.read_csv(path, sep= ' ')
    print(df)


