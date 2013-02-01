# -*- coding: cp1251 -*-
'''
Created on 20.12.2012

@author: Shcheblykin
'''

import sys
from PyQt4 import QtGui
# from PyQt4 import QtCore
from PyQt4.QtCore import Qt
# from PyQt4 import QtCore

import pylab
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import \
#    NavigationToolbar2QTAgg as NavigationToolbar
# from matplotlib.figure import Figure

import mySpreadsheet


class TabAdjust(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        hbox = QtGui.QHBoxLayout(self)
        grid = QtGui.QGridLayout()
        self.adjTable = mySpreadsheet.MySpreadsheet()
        self.adjTable.horizontalHeaderItem(0).setText(u"Uвых, В")
        self.adjTable.horizontalHeaderItem(1).setText(u"Uацп")
        self.adjTable.horizontalHeaderItem(2).setText(u"Iацп")
        
        self.pAdd = QtGui.QPushButton(u'Добавить')
        self.pDel = QtGui.QPushButton(u'Удалить')
        
        # для всех LineEdit отключим контекстное меню
        # .setContextMenuPolicy(Qt.NoContextMenu)
        
        # создадим поле для ввоода значения напряжения
        # это должно быть целое число от 1 до 100В
        self.entValU = QtGui.QLineEdit(u'Uвых')
        self.entValU.setValidator(QtGui.QIntValidator(1, 100, self))
        self.entValU.clear()  # очистка текста
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.readValU = QtGui.QLineEdit(u'Нет данных')
        self.readValU.setDisabled(True)
        self.readValU.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.readValI1 = QtGui.QLineEdit(u'Нет данных')
        self.readValI1.setDisabled(True)
        self.readValI1.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.readValI2 = QtGui.QLineEdit(u'Нет данных')
        self.readValI2.setDisabled(True)
        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.readValU48 = QtGui.QLineEdit(u'Нет данных')
        self.readValU48.setDisabled(True)
        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.readValUwork = QtGui.QLineEdit(u'Нет данных')
        self.readValUwork.setDisabled(True)
        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
        
        # создаем область для графика
        self.figure = pylab.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(400, 400)
        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
        self.axes.set_title('Haba-haba')
        
        grid.addWidget(self.adjTable, 0, 0, 1, 2)
        
        # входное напряжение
        grid.addWidget(QtGui.QLabel(u'Напряжение выхода, В'), 1, 0, 1, 2,
                       Qt.AlignCenter)
        grid.addWidget(self.entValU, 2, 1)
        grid.addWidget(self.pAdd, 2, 0)
        
        # показания АЦП
        grid.addWidget(QtGui.QLabel(u'Показания АЦП'), 3, 0, 1, 2,
                       Qt.AlignCenter)

        grid.addWidget(QtGui.QLabel(u'Напряжение выхода'), 4, 0,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU, 4, 1)
        
        grid.addWidget(QtGui.QLabel(u'Ток выхода 1'), 5, 0,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI1, 5, 1)
        
        grid.addWidget(QtGui.QLabel(u'Ток выхода 2'), 6, 0,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI2, 6, 1)
        
        grid.addWidget(QtGui.QLabel(u'Напряжение питания'), 7, 0,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU48, 7, 1)
        
        grid.addWidget(QtGui.QLabel(u'Напряжение раб.т'), 8, 0,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValUwork, 8, 1)
        
        hbox.addLayout(grid)
        hbox.addWidget(self.canvas)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabAdjust()
    my_frame.show()
    
    app.exec_()
