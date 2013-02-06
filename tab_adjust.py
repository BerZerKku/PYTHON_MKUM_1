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

# import pylab
# from matplotlib.backends.backend_qt4agg import \
#    FigureCanvasQTAgg as FigureCanvas
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
        self.adjTable.horizontalHeaderItem(0).setText(u"U���, �")
        self.adjTable.horizontalHeaderItem(1).setText(u"U���")
        self.adjTable.horizontalHeaderItem(2).setText(u"I���")
#        self.adjTable.clearTable()
        
        self.pAdd = QtGui.QPushButton(u'��������')
        self.pAdd.setDisabled(True)
        self.pAdd.clicked.connect(self.addPointToTable)
        
#        self.pDel = QtGui.QPushButton(u'�������')
        
        # ��� ���� LineEdit �������� ����������� ����
        # .setContextMenuPolicy(Qt.NoContextMenu)
        
        # �������� ���� ��� ������ �������� ����������
        # ��� ������ ���� ����� ����� �� 1 �� 100�
        self.entValU = QtGui.QLineEdit(u'U���')
        self.entValU.setValidator(QtGui.QIntValidator(1, 100, self))
        self.entValU.clear()  # ������� ������
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.entValU.textChanged.connect(self.valUChange)
      
        self.readValU = QtGui.QLineEdit(u'��� ������')
        self.readValU.setDisabled(True)
        self.readValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValU = QtGui.QCheckBox()
        self.checkValU.setChecked(True)
        self.checkValU.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValI1 = QtGui.QLineEdit(u'��� ������')
        self.readValI1.setDisabled(True)
        self.readValI1.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValI1 = QtGui.QCheckBox()
        self.checkValI1.setChecked(True)
        self.checkValI1.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValI2 = QtGui.QLineEdit(u'��� ������')
        self.readValI2.setDisabled(True)
        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValI2 = QtGui.QCheckBox()
        self.checkValI2.setChecked(False)
        self.checkValI2.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValU48 = QtGui.QLineEdit(u'��� ������')
        self.readValU48.setDisabled(True)
        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValU48 = QtGui.QCheckBox()
        self.checkValU48.setChecked(False)
        self.checkValU48.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValUwork = QtGui.QLineEdit(u'��� ������')
        self.readValUwork.setDisabled(True)
        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValUwork = QtGui.QCheckBox()
        self.checkValUwork.setChecked(False)
        self.checkValUwork.setToolTip(u"���./����. ���������� ���������.")
        
        self.pSave = QtGui.QPushButton(u'���������')
        self.pSave.setDisabled(True)
        
        self.pSaveAs = QtGui.QPushButton(u'��������� ���...')
        self.pSaveAs.setDisabled(True)
        
        # ������� ������� ��� �������
#        self.figure = pylab.figure()
#        self.canvas = FigureCanvas(self.figure)
#        self.canvas.setFixedSize(400, 400)
#        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
#        self.axes.set_title('Haba-haba')
        
        # ��������� ������� � �����
        grid.addWidget(self.adjTable, 0, 0, 7, 2)
        
        grid.addWidget(self.pSave, 7, 0)
        grid.addWidget(self.pSaveAs, 7, 1)
        
        # ��������� ��������� ��� ����� ������
        col = 2
        row = 0
        
        # ������� ����������
        grid.addWidget(QtGui.QLabel(u'���������� ������, �'), row, col, 1, 2,
                       Qt.AlignCenter)
        row += 1
        grid.addWidget(self.entValU, row, col)
        grid.addWidget(self.pAdd, row, col + 1)
        
        # ��������� ���
        row += 1
        grid.addWidget(QtGui.QLabel(u'��������� ���'), row, col, 1, 2,
                       Qt.AlignCenter)
        
        #     ���������� ������
        row += 1
        grid.addWidget(QtGui.QLabel(u'���������� ������'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU, row, col + 1)
        grid.addWidget(self.checkValU, row, col + 2)
        
        #     ��� ������ 1
        row += 1
        grid.addWidget(QtGui.QLabel(u'��� ������ 1'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI1, row, col + 1)
        grid.addWidget(self.checkValI1, row, col + 2)
        
        #     ��� ������ 2
        row += 1
        grid.addWidget(QtGui.QLabel(u'��� ������ 2'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI2, row, col + 1)
        grid.addWidget(self.checkValI2, row, col + 2)
        
        #     ���������� �������
        row += 1
        grid.addWidget(QtGui.QLabel(u'���������� �������'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU48, row, col + 1)
        grid.addWidget(self.checkValU48, row, col + 2)
        
        #     ���������� � ������� �����
        row += 1
        grid.addWidget(QtGui.QLabel(u'���������� ���.�'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValUwork, row, col + 1)
        grid.addWidget(self.checkValUwork, row, col + 2)
        
        hbox.addLayout(grid)
#        hbox.addWidget(self.canvas)
    
    def addPointToTable(self):
        ''' (self) -> None [SLOT]
            
            ���������� ����� ������ � ������� ������
        '''
        
        # ���� ���������
        error = False
        
        # ������� � �������� ��������� ������
        # ���� �� ��������� �������� ���� error ����� True
        # ���������� ������ �� ����������
        valUout = self.entValU.text()
        
        valU = 0
        if self.checkValU.isChecked():
            flag, valU = self.checkValue(self.readValU.text())
            if not flag:
                print '������ �������� ��� "��������� ������"'
                error = True
        
        valI1 = 0
        if self.checkValI1.isChecked():
            flag, valI1 = self.checkValue(self.readValI1.text())
            if not flag:
                print '������ �������� ��� "��� ������ 1"'
                error = True
        
        valI2 = 0
        if self.checkValI2.isChecked():
            flag, valI2 = self.checkValue(self.readValI2.text())
            if not flag:
                print '������ �������� ��� "��� ������ 2"'
                error = True
        
        valU48 = 0
        if self.checkValU48.isChecked():
            flag, valU48 = self.checkValue(self.readValU48.text())
            if not flag:
                print '������ �������� ��� "���������� �������"'
                error = True
        
        valUwork = 0
        if self.checkValUwork.isChecked():
            flag, valUwork = self.checkValue(self.readValUwork.text())
            if not flag:
                print '������ �������� ��� "���������� ������� �����"'
                error = True
        
        # ���� ���� ������
        if error:
            return
        
        data = [valUout, valU, valI1]
        self.adjTable.addRowData(data)
                   
    def valUChange(self, val):
        ''' (self, str) -> None [SLOT]
        
            ������� �� ����/��������� ����������. ��� ���������� ������ � ����
            ����������� ����������� ���������� ����� ������.
        '''
        if len(val) > 0:
            self.pAdd.setEnabled(True)
        else:
            self.pAdd.setDisabled(True)

    def checkValue(self, text):
        ''' (self, str) -> bool, int
        
            ������� ������ ������������� � ����� val. ���� ���������� ��������
            ������� �� �������� 0..1023, ������������ False, val.
            ����� True, val.
        '''
        
        sost = False
        
        try:
            val = int(text)
        
            if val >= 0 and val <= 1023:
                sost = True
        except:
            print self, '������ �������������� ������ � int'
            val = 0
        
        return sost, val
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabAdjust()
    my_frame.show()
    
    # ��������� ��� �����������
    QtGui.QApplication.setStyle('Cleanlooks')
    
    app.exec_()
