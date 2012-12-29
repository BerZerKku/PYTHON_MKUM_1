# -*- coding: cp1251 -*-
'''
Created on 20.12.2012

@author: Shcheblykin
'''

import sys
from PyQt4 import QtGui
# from PyQt4 import QtCore

import pylab
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QTAgg as NavigationToolbar
# from matplotlib.figure import Figure

import mySpreadsheet


class TabAdjust(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        grid = QtGui.QGridLayout(self)
        self.adjTable = mySpreadsheet.MySpreadsheet()
        self.pAdd = QtGui.QPushButton(u'Добавить')
        self.pDel = QtGui.QPushButton(u'Удалить')
        self.entValU = QtGui.QLineEdit(u'Uвых')
        self.entValU.setInputMask("99")
        self.entValU.clear()
        self.entValU.setText('')
        self.readValU = QtGui.QLineEdit(u'АЦП Uвых')
        self.readValU.setReadOnly(True)
        self.readValI1 = QtGui.QLineEdit(u'АЦП Iвых1')
        self.readValI1.setReadOnly(True)
        self.readValI2 = QtGui.QLineEdit(u'АЦП Iвых2')
        self.readValI2.setReadOnly(True)
        self.readValU48 = QtGui.QLineEdit(u'АЦП Uпитания')
        self.readValU48.setReadOnly(True)
        self.readValUwork = QtGui.QLineEdit(u'АЦП Uраб.точки')
        self.readValUwork.setReadOnly(True)
        
        # создаем область для графика
        self.figure = pylab.figure()
        self.figure.set
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(400, 400)
        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
        self.axes.set_title('Haba-haba')
        
        grid.addWidget(self.adjTable, 0, 0, 1, 2)
        grid.addWidget(self.canvas, 0, 2, 5, 2)
#        grid.addWidget(self.debugTE, 0, 2, 5, 2)
        grid.addWidget(self.pAdd, 1, 0)
        grid.addWidget(self.pDel, 1, 1)
        grid.addWidget(self.entValU, 2, 0)
        grid.addWidget(self.readValU, 2, 1)
        grid.addWidget(self.readValI1, 3, 0)
        grid.addWidget(self.readValI2, 3, 1)
        grid.addWidget(self.readValU48, 4, 0)
        grid.addWidget(self.readValUwork, 4, 1)
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabAdjust()
    my_frame.show()
    
    app.exec_()
