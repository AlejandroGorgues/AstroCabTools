import os
import sys

import pytestqt
import pytest
from pytestqt.qt_compat import qt_api

#from fit_line.src import plotSelection as plt

"""def test_basic(qtbot, tmpdir):

    tmpdir.join('spectrum.txt').ensure()

    plotSelection = plt.MrsPltList()
    plotSelection.show()
    plotSelection.open()

    qtbot.addWidget(plotSelection)
    qtbot.mouseClick(plotSelection.fileButton,qt_api.QtCore.Qt.LeftButton)
    plotSelection.redshift_line.setText('3.2')
    assert os.path.basename(plotSelection.spectrumPath)== 'nucleo.txt'
    assert plotSelection.redshift_line.text() == '3.2'"""
