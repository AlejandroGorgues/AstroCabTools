from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt


#Create custom TabBar class widget
class CustomTabBarWidget(QtWidgets.QTabBar):

    #Initialize size of each tabBar based on kwargs named arguments
    def __init__(self, parent=None, **kwargs):
        self.tabSize = QtCore.QSize(kwargs.pop(
            'width'), kwargs.pop('height'))
        QtWidgets.QTabBar.__init__(self, parent, **kwargs)


    #The PaintEvent, wich is overrrided, it defines for each text in tab, the style as well as alignment
    #This event is called after all tabs are defined and need to be painted
    #Because of that, self.count() returns the number of text which is the number of tabs
    #And self.text returns the all texts in a list with the same size as the self.count() value shows
    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        #For each one, it moves the text to the left of the tab, draw it inside a recangle shape,
        #And align it to the vertical center
        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, Qt.AlignVCenter |
                            Qt.TextDontClip,
                            self.tabText(index))
        painter.end()

    #Overrides the size for each tab with the one that has been defined previously in the init method
    def tabSizeHint(self, index):
        return self.tabSize
