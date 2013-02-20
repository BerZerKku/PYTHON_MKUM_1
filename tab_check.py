# -*- coding: cp1251 -*-
'''
Created on 20.12.2012

@author: Shcheblykin
'''

import sys
import my_func
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
# from PyQt4 import QtCore

# import pylab
# from matplotlib.backends.backend_qt4agg import \
#    FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import \
#    NavigationToolbar2QTAgg as NavigationToolbar
# from matplotlib.figure import Figure

import mySpreadsheet


class TabCheck(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        hbox = QtGui.QHBoxLayout(self)
        grid = QtGui.QGridLayout()
        self.adjTable = mySpreadsheet.MySpreadsheet(row=6, column=5)
        self.adjTable.setFixedSize(280, 200)
        self.adjTable.horizontalHeaderItem(0).setText(u"U���,�")
        self.adjTable.horizontalHeaderItem(1).setText(u"U���,�")
        self.adjTable.horizontalHeaderItem(2).setText(u"I���,��")
        self.adjTable.horizontalHeaderItem(3).setText(u"I���,��")
        self.adjTable.horizontalHeaderItem(4).setText(u"R���,��")
        self.adjTable.clearTable()
        self.connect(self.adjTable, QtCore.SIGNAL('changeData(QString)'),
                     self.valUChange)
        
        self.pAdd = QtGui.QPushButton(u'��������')
        self.pAdd.setDisabled(True)
        self.pAdd.clicked.connect(self.addPointToTable)
        
#        self.pDel = QtGui.QPushButton(u'�������')
        
        # ��� ���� LineEdit �������� ����������� ����
        # .setContextMenuPolicy(Qt.NoContextMenu)
        
        # �������� ���� ��� ������ �������� ����������
        # ��� ������ ���� ����� ����� �� 1 �� 100�
#        self.entValU = QtGui.QLineEdit(u'U���')
#        self.entValU.setValidator(QtGui.QDoubleValidator(1, 99, 1, self))
#        self.entValU.clear()  # ������� ������
        self.entValU = QtGui.QDoubleSpinBox()
        self.entValU.setRange(0.0, 100.0)
        self.entValU.setDecimals(1)
        #    ������ ����������� ����, �.�. ����� ���� �������� � 'Undo'
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
#        self.entValU.textChanged.connect(self.valUChange)
        self.entValU.valueChanged.connect(self.valUChange)
          
        self.readValU = QtGui.QLineEdit(u'��� ������')
        self.readValU.setDisabled(True)
#        self.readValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValU = QtGui.QCheckBox()
        self.checkValU.setChecked(True)
        self.checkValU.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValI1 = QtGui.QLineEdit(u'��� ������')
        self.readValI1.setDisabled(True)
#        self.readValI1.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValI1 = QtGui.QCheckBox()
        self.checkValI1.setChecked(True)
        self.checkValI1.setToolTip(u"���./����. ���������� ���������.")
        
        self.readValR = QtGui.QLineEdit(u'��� ������')
        self.readValR.setDisabled(True)
#        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValR = QtGui.QCheckBox()
        self.checkValR.setChecked(True)
        self.checkValR.setToolTip(u"���./����. ���������� ���������.")
        
#        self.readValU48 = QtGui.QLineEdit(u'��� ������')
#        self.readValU48.setDisabled(True)
# #        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValU48 = QtGui.QCheckBox()
#        self.checkValU48.setChecked(False)
#        self.checkValU48.setDisabled(True)
#        self.checkValU48.setToolTip(u"���./����. ���������� ���������.")

#        self.readValUwork = QtGui.QLineEdit(u'��� ������')
#        self.readValUwork.setDisabled(True)
# #        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValUwork = QtGui.QCheckBox()
#        self.checkValUwork.setChecked(False)
#        self.checkValUwork.setDisabled(True)
#        self.checkValUwork.setToolTip(u"���./����. ���������� ���������.")
        
        self.pSave = QtGui.QPushButton(u'���������')
        self.pSave.clicked.connect(self.saveFile)
        self.pSave.setDisabled(True)
        
        self.pSaveAs = QtGui.QPushButton(u'��������� ���...')
        self.pSaveAs.clicked.connect(self.saveFileAs)
        self.pSaveAs.setDisabled(True)
        
        self.pOpen = QtGui.QPushButton(u'�������...')
        self.pOpen.clicked.connect(self.openFile)
        self.pOpen.setEnabled(True)
        
        # ������� ������� ��� �������
#        self.figure = pylab.figure()
#        self.canvas = FigureCanvas(self.figure)
#        self.canvas.setFixedSize(400, 400)
#        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
#        self.axes.set_title('Haba-haba')
        
        # ��������� ������� � �����
        grid.addWidget(self.adjTable, 0, 0, 7, 2)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.pOpen)
        hbox1.addWidget(self.pSave)
        hbox1.addWidget(self.pSaveAs)
#        grid.addWidget(self.pSave, 7, 0)
#        grid.addWidget(self.pSaveAs, 7, 1)
        grid.addLayout(hbox1, 7, 0, 1, 2)
        
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
        grid.addWidget(QtGui.QLabel(u'���������� ������, �'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU, row, col + 1)
        grid.addWidget(self.checkValU, row, col + 2)
        
        #     ��� ������ 1
        row += 1
        grid.addWidget(QtGui.QLabel(u'��� ������, ��'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI1, row, col + 1)
        grid.addWidget(self.checkValI1, row, col + 2)
        
        #     �������������
        row += 1
        grid.addWidget(QtGui.QLabel(u'�������������, ��'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValR, row, col + 1)
        grid.addWidget(self.checkValR, row, col + 2)
        
        #     ���������� �������
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'���������� �������, �'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValU48, row, col + 1)
#        grid.addWidget(self.checkValU48, row, col + 2)
       
#        #     ���������� � ������� �����
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'���������� ���.�� �'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValUwork, row, col + 1)
#        grid.addWidget(self.checkValUwork, row, col + 2)
        
        hbox.addLayout(grid)
#        hbox.addWidget(self.canvas)
        
        # ������ 200�� ����� ��������� ����������� ����� ����� ��������
#        self.timer = QtCore.QTimer()
#        self.timer.start(200)
#        self.timer.timeout.connect(self.valUChange)
        
    def addPointToTable(self):
        ''' (self) -> None [SLOT]
            
            ���������� ����� ������ � ������� ������
        '''
        
        # ���� ���������
        error = False
        
        # ������� � �������� ��������� ������
        # ���� �� ��������� �������� ���� error ����� True
        # ���������� ������ �� ����������
        flag, valUout = self.checkValue(self.entValU.text(), 1, 99)
#        self.entValU.setText("")
        if not flag:
            print u"������ ���������� �������� ���������� ������"
            error = True
            
        valU = 0
        if self.checkValU.isChecked():
            flag, valU = self.checkValue(self.readValU.text(), 1, 99)
            if not flag:
                print u'������ �������� ��� "��������� ������"'
                error = True
        
        valI1 = 0
        if self.checkValI1.isChecked():
            flag, valI1 = self.checkValue(self.readValI1.text(), 1, 1500)
            if not flag:
                print u'������ �������� ��� "��� ������ 1"'
                error = True
            else:
                valI1 = int(valI1)
        
        valI1ent = int(round((valUout * 1000) / 75.0))
        
        valR = 0
        if self.checkValR.isChecked():
            flag, valR = self.checkValue(self.readValR.text(), 1, 999)
            if not flag:
                print u'������ �������� ��� "�������������"'
                error = True
        
#        valI2 = 0
#        if self.checkValI2.isChecked():
#            flag, valI2 = self.checkValue(self.readValI2.text())
#            if not flag:
#                print u'������ �������� ��� "��� ������ 2"'
#                error = True
     
#        valU48 = 0
#        if self.checkValU48.isChecked():
#            flag, valU48 = self.checkValue(self.readValU48.text())
#            if not flag:
#                print u'������ �������� ��� "���������� �������"'
#                error = True
       
#        valUwork = 0
#        if self.checkValUwork.isChecked():
#            flag, valUwork = self.checkValue(self.readValUwork.text())
#            if not flag:
#                print u'������ �������� ��� "���������� ������� �����"'
#                error = True
        
        # ���� ���� ������
        if error:
            QtGui.QMessageBox.warning(self, u'������ �����',
                                      u'������������ ������ ���.')
            return
        
        # ������� ������, � ������� ���� �����
        data = [valUout, valU, valI1ent, valI1, valR]
        self.adjTable.addRowData(data)
        
        if self.adjTable.isFull():
            self.pAdd.setDisabled(True)
            self.pSave.setEnabled(True)
            self.pSaveAs.setEnabled(True)
                   
    def valUChange(self, val=""):
        ''' (self, str) -> None
        
            ������� �� ����/��������� ����������. ��� ���������� ������ � ����
            ����������� ����������� ���������� ����� ������. ��� �����������
            �������, ���������� ����������� ��������� ��������.
        '''

        val = self.entValU.text()
        if self.adjTable.isFull():
            # ������� ������, �������� ����������� ���������� ������
            # � �������� ���������� ��������
            self.pAdd.setDisabled(True)
            self.pSave.setEnabled(True)
            self.pSaveAs.setEnabled(True)
        else:
            # ������� �� ������, �������� ����������� ���������� ���������
            # � �������� ������ � ���� ����� ����������
            self.pSave.setDisabled(True)
            self.pSaveAs.setDisabled(True)
            if len(val) == 0:
                self.pAdd.setDisabled(True)
            else:
                self.pAdd.setEnabled(True)
            
    def checkValue(self, val, minVal, maxVal):
        ''' (self, str, number, number) -> bool, float
        
            ������� ������ ������������� � ����� val. ���� ���������� ��������
            ������� �� �������� min <= val <= max, ������������ False, val.
            ����� True, val.
            
            >>> .checkValue("123.7", 1, 99)
            (False, 0)
            >>> .checkValue("123.7", 1, 199)
            (True, 123.7)
        '''
        
        sost = False
        
        try:
            # ��� ������� �������������� ������� � ������, ������� �� �����
            val = val.replace(',', '.')
            val = float(val)
            sost = True
        except:
            print u"Error:",
            print u'������ �������������� ������ � float', self
            val = 0

        if sost:
            if not (val >= minVal and val <= maxVal):
                val = 0
                sost = False
        
        return sost, val
    
    def openFile(self):
        ''' (self) -> None
            
            �������� ����� ������ � ����������� ����������� �������.
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, u"�������",
                                        filter="Data Files (*.dat)")
        
        if not filename:
            return
        
        # ���������� ����������� �����
        f = open(filename, 'rb')
        data_bin = f.read()
        f.close()
        
        data = []
        for char in data_bin:
            data.append(char.encode('hex').upper())
        del data_bin
        
        # �������������
        r = my_func.strHexToInt(data[0])
        print r
        
        # ���������� ���������� ��������
        uOut = []
        for i in range(6):
            u = my_func.strHexToInt(data[i + 1])
            if u == 0:
                break
            uOut.append(u)
        print uOut
        
        # ��� ���������� ��������
        if r == 0:
            print u'Error:'
            print u'��������� ������������� �� ����� ����� 0'
            raise ValueError
        iOut = []
        for u in uOut:
            iOut.append(int(round(u * 1000 / r)))
        print iOut
        
        # ��� 
        
         
    def saveFileAs(self):
        ''' (self) -> None
            
            ���������� ����� � ������� ������� "��������� ���...".
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, u"��������� ���...",
                                        filter="Data Files (*.dat)")
        if filename:
            self.saveFile(name=filename)
    
    def saveFile(self, chacked=False, name='MkUM.dat'):
        ''' (self, name) -> None
            
            ���������� ����� ������ � �����/������� name
            chacked - ��� SIGNAL �� ������
        '''
        # ������� ���� �������� � �������� �� �� ������
        pass
  
    def intToHex(self, val):
        ''' (self, int) -> str
        
            �������������� int � ������ hex. ������� ������ ������.
            
            >>> .intToHex(5)
            '0500'
            >>> .intToHex(270)
            '0E01'
        '''
        # �������������� int � ������
        val = '%.4x' % int(val)
        val = val.upper()
        # ���������� ������ �� ������� � ������� "�����"
        hi = val[:2]
        low = val[2:]
        # ������� ����� ������, ������� ������ ������
        val = low + hi
        
        return val
    
    def calcCRC(self, data):
        ''' (self, str) -> str
        
            ���������� CRC. ���������� ����� ���� ��� ����� �� ������ 256 �
            ����������� ��������� � �������������� ������
            
            >>>.calcCRC(':1007D00091789A998141E17A543F2B0005005800')
            'A5'
            
            >>>.calcCRC(':1007E0000A00B30014000E011E00270042004F00')
            '53'
        '''
        # ��� ������� �������� ������ ������, ������ ���
        tmp = data
        if tmp[0] == ':':
            tmp = tmp[1:]
        
        # � ������ ������ ���� ������ ���-�� ��������
        if len(tmp) % 2 != 0:
            print "calcCRC exception. Data = %s" % data
            raise
        
        crc = 0
        while len(tmp) > 0:
            crc += int(tmp[:2], 16)
            tmp = tmp[2:]
        
        crc = "%.2x" % (256 - (crc % 256))
        return crc.upper()
        
#    def debugSaveFile(self, data):
#        ''' (self) -> None
      
#            ���������� ����� ��� �������.
#        '''
#        for i in range(self.adjTable.rowCount()):
#            self.adjTable.item(i, 0).setText(str(data[0][i * 2 + 1]))
#            self.adjTable.item(i, 1).setText(str(data[0][i * 2]))
#            self.adjTable.item(i, 2).setText(str(data[1][i * 2]))
        
#        self.pSave.setEnabled(True)
#        self.pSaveAs.setEnabled(True)
            
            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabCheck()
    my_frame.show()
    
    # data 1
    # my_frame.debugSaveFile([[43, 5, 88, 10, 179, 20, 270, 30],
    #                        [39, 66, 79, 133, 159, 266, 242, 400]])
#    my_frame.debugSaveFile([[40, 5, 81, 10, 172, 20, 263, 30],
#                            [45, 66, 90, 133, 187, 266, 283, 400]])
    
    # ��������� ��� �����������
    QtGui.QApplication.setStyle('Cleanlooks')
    
    app.exec_()


# import unittest
#
#
# class TestTabCheck(unittest.TestCase):
#    """${short_summary_of_testcase}
#    """
#    def setUp(self):
# #        self.testFrame = TabCheck()
#        self.app = QtGui.QApplication(sys.argv)
#        self.form = TabCheck()

#    def tearDown(self):
#        """${no_tearDown_required}
#        """
#    pass  # skip tearDown
#
#    def testIntToHex(self):
#        """${short_description_of_test}
#        """
# #        print self.testFrame
#        self.assertEqual(self.form.intToHex(5), '0500')
#        self.assertEqual(self.form.intToHex(270), '0E01')

#    def testCalcCRC(self):
#        self.assertEqual(
#                self.form.calcCRC(':1007D00091789A998141E17A543F2B0005005800')
#                ,'A5')
#        self.assertEqual(
#                self.form.calcCRC(':1007E0000A00B30014000E011E00270042004F00')
#                ,'53')
