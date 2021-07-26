#-*- coding: utf-8 -*-
"""
Method that applied redshift to flux and wavelength
"""
import numpy as np
import pandas as pd
import copy
import re

import sys
import io

def get_data_from_txt(path):
    """
    Obtain the wavelenth and flux values from an ascii file
    :param str path: path of the sprectrum file
    """

    spectra = pd.read_csv(path, delimiter=' ', header=0)

    #Because the first and second column are always wavelength and flux column
    #I can get the units from them
    wUnits = spectra.columns[0]
    fUnits = spectra.columns[1]

    wavelength_cols = []
    flux_cols = []

    while not spectra.empty:
        flux_part = []
        if 'Wavelength' in spectra.columns[0]:
            wavelength_cols.append(copy.deepcopy(spectra.iloc[:,0]))
            spectra.drop(spectra.columns[0], axis=1, inplace=True)

        while True:
            if spectra.empty:
                break
            elif 'Wavelength' in spectra.columns[0]:
                break
            else:
                flux_part.append(copy.deepcopy(spectra.iloc[:,0]))
                spectra.drop(spectra.columns[0], axis=1, inplace=True)

        flux_cols.append(flux_part)

    #Pattern to extract the units from the flux and wavelength text
    r_units = re.compile('(?!\w+)\((.*)\)')

    #Pattern to get every word
    r_id = re.compile('^(\w*)')

    m = r_units.search(wUnits)
    if m: wUnits= m.group(1)

    m = r_units.search(fUnits)
    if m: fUnits = m.group(1)

    for flux_group in flux_cols:
        for col in flux_group:
            m = r_id.match(col.name)
            #if m: flux_group.rename(columns= {col.name:m.group(1)}, inplace = True)
            if m: col.rename(m.group(1))

    return wavelength_cols, flux_cols, wUnits, fUnits
