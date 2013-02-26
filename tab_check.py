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
            ���� ���������� ���������� �������� = 0, �� ������ ������������.
            � ������ ������ ������ ������ ���� ������������� = 75��.
            � ����� ��������� �������� � ������ ������ ���� 1.
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
            data.append(my_func.charToStrHex(char))
        del data_bin
        
        # �������������
        try:
            r = my_func.strHexToInt(data[0])
        except:
            return
        
        # ������� �������� - ������ 1, ����� 2
        # � ����� ��������� ������ ������ ���� 0
        if r == 0:
            self.newData(data)
        else:
            self.oldData(data)
   
    def newData(self, data):
        ''' (self, list) -> bool
        
            �������� ����� ������ ������ �������.
        '''
        print data
        
        r = my_func.strHexToInt(data[1])
        print r
        
        uOut = []
        for i in range(self.adjTable.rowCount()):
            val = ''.join(data[2 + i * 4: 2 + i * 4 + 4])
            uOut.append(my_func.strHexToFloat(val, 'le'))
        print uOut
        
        uOut = []
        uOutADC = []
        iOut = []
        iOutADC = []
        rOutADC = []
        
        offset = 2
        for i in range(self.adjTable.rowCount()):
            val = ''.join(data[offset: offset + 4])
            offset += 4
            uOut.append(round(my_func.strHexToFloat(val, 'le'), 1))
            
            val = ''.join(data[offset: offset + 4])
            offset += 4
            uOutADC.append(round(my_func.strHexToFloat(val, 'le'), 1))
            
            val = ''.join(data[offset: offset + 2])
            offset += 2
            iOut.append(my_func.strHexToInt(val, 'le'))
            
            val = ''.join(data[offset: offset + 2])
            offset += 2
            iOutADC.append(my_func.strHexToInt(val, 'le'))
            
            val = ''.join(data[offset: offset + 4])
            offset += 4
            rOutADC.append(round(my_func.strHexToFloat(val, 'le'), 1))
            
        # ���������� ������� ����������� �������
        self.adjTable.clearTable()
        for i in range(len(uOut)):
            data = [uOut[i], uOutADC[i], iOut[i], iOutADC[i], r]
            self.adjTable.addRowData(data)
         
    def oldData(self, data):
        ''' (self, list) -> bool
            
            �������� ����� ������ ������� �������.
        '''
        # �������������
        r = my_func.strHexToInt(data[0])
        
        # ���-�� ��������� ��� ����������
        numValues = self.adjTable.rowCount()
        
        # ���������� ���������� ��������
        uOut = []
        try:
            for i in range(numValues):
                u = my_func.strHexToInt(data[i + 1])
                if u == 0:
                    break
                uOut.append(float(u))
#            print u"Volatages =", uOut
        except:
            return
        
        # ��� ���������� ��������
        iOut = []
        for u in uOut:
            iOut.append(int(round(u * 1000 / r)))
#        print u"Currents =", iOut
        
        # ���������� ���������� ����
        uOutADC = []
        try:
            for i in range(numValues):
                tmp = data[41 + i * 4: 41 + i * 4 + 4]
                tmp = ''.join(tmp)
                tmp = round(my_func.strHexToFloat(tmp, 'le'), 1)
                uOutADC.append(tmp)
        except:
            return
#        print u"ADC vlotages =", uOutADC
        
        # ��� ���������� ����
        iOutADC = []
        try:
            for i in range(numValues):
                tmp = data[201 + i * 2: 201 + i * 2 + 2]
                tmp = ''.join(tmp)
                tmp = my_func.strHexToInt(tmp, 'le')
                iOutADC.append(tmp)
        except:
            return
#        print u'ADC currents =', iOutADC
        
        # ������������� ���������� ����
        rOutADC = []
        for i in range(numValues):
            if iOutADC[i] != 0:
                tmp = round((1000 * uOutADC[i]) / iOutADC[i], 1)
            else:
                tmp = 1
            rOutADC.append(tmp)
#        print u"ADC resistances =", rOutADC
        
        # ���������� ������� ����������� �������
        self.adjTable.clearTable()
        for i in range(len(uOut)):
            data = [uOut[i], uOutADC[i], iOut[i], iOutADC[i], r]
            self.adjTable.addRowData(data)
        
    def saveFileAs(self):
        ''' (self) -> None
            
            ���������� ����� � ������� ������� "��������� ���...".
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, u"��������� ���...",
                                        filter="Data Files (*.dat)")
        if filename:
            self.saveFile(name=filename)
    
    def saveFile(self, chacked=False, name='check.dat'):
        ''' (self, name) -> None
            
            ���������� ����� ������ � �����/������� name
            chacked - ��� SIGNAL �� ������
        '''
        # ������� ���� �������� � �������� �� �� ������
        
        data = ['00', ]
        data.append(my_func.intToStrHex(75))
        
        for i in range(self.adjTable.rowCount()):
            val = float(self.adjTable.item(i, 0).text())
            data.append(my_func.floatToStrHex(val, 'le'))
        
#        for i in range(self.adjTable.rowCount()):
            val = float(self.adjTable.item(i, 1).text())
            data.append(my_func.floatToStrHex(val, 'le'))
            
#        for i in range(self.adjTable.rowCount()):
            val = int(self.adjTable.item(i, 2).text())
            data.append(my_func.intToStrHex(val, 4, 'le'))
            
#        for i in range(self.adjTable.rowCount()):
            val = int(self.adjTable.item(i, 3).text())
            data.append(my_func.intToStrHex(val, 4, 'le'))
            
#        for i in range(self.adjTable.rowCount()):
            val = float(self.adjTable.item(i, 4).text())
            data.append(my_func.floatToStrHex(val, 'le'))
        
        # bin-file
        fSave = open(name, 'wb')
        for val in data:
            tmp = val.decode('hex')
            fSave.write(tmp)
        fSave.close()
  
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
    
    # ������������ ������ - �������. ���������� ��������� � �������.
    def checkTolerance(self, ref, val, warn=0.05, err=0.1):
        ''' (num, num, float, float) -> Qt.[color]
            
            �������� ���������� ����������� �� ��������� (�������� ��������)
            "��������������" warn � ������ err.
            � ����������� �� ����� ���������� ����:
            ������� - ����, ������ ��������������, ������� - ������.
            �������� ����� ���� ��� ������, ��� � �������.
            
            @param ref ��������� ��������
            @param val ���������� ��������
            @param warn ����� ��������������, �������� 0.05 ��� 5%
            @param err ����� ������, �������� 0.10 ��� 10%
            
            @return ����
            @arg Qt.red
            @arg Qt.green
            @arg Qt.yellow
        '''
        try:
            ref = float(ref)
        except:
            txt = u"Error: ��������� ��� ������ ref,", type(ref)
            raise TypeError(txt)
        
        try:
            val = float(val)
        except:
            txt = u"Error: ��������� ��� ������ val,", type(val)
            raise TypeError(txt)
        
        try:
            warn = float(warn)
        except:
            txt = u"Error: ��������� ��� ������ warn,", type(warn)
            raise TypeError(txt)
            
        try:
            err = float(err)
        except:
            txt = u"Error: ��������� ��� ������ err,", type(err)
            raise TypeError(txt)
            
        tmp = abs((ref - val) / ref)
        if  tmp >= err:
            color = Qt.red
        elif tmp >= warn:
            color = Qt.yellow
        else:
            color = Qt.green
            
        return color
            
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
#    my_frame.debugSaveFile([[43, 5, 88, 10, 179, 20, 270, 30],
#                        [39, 66, 79, 133, 159, 266, 242, 400]])
#    my_frame.debugSaveFile([[40, 5, 81, 10, 172, 20, 263, 30],
#                            [45, 66, 90, 133, 187, 266, 283, 400]])

    # ��������� ��� �����������
    QtGui.QApplication.setStyle('Cleanlooks')
   
    app.exec_()


import unittest


class TestTabCheck(unittest.TestCase):
    """${short_summary_of_testcase}
    """
    def setUp(self):
        app = QtGui.QApplication(sys.argv)
        self.form = TabCheck()

    def tearDown(self):
        """${no_tearDown_required}
        """
        pass  # skip tearDown

    def testIntToHex(self):
        """${short_description_of_test}
        """
        self.assertEqual(self.form.intToHex(5), '0500')
        self.assertEqual(self.form.intToHex(270), '0E01')
        
    def testCheckTolerance(self):
        '''
            �������� ������� checkTolerance�
        '''
        self.assertEqual(self.form.checkTolerance(100, 96), Qt.green)
        self.assertEqual(self.form.checkTolerance("100", "97"), Qt.green)
        self.assertEqual(self.form.checkTolerance(100, 95), Qt.yellow)
        self.assertEqual(self.form.checkTolerance(100, 90), Qt.red)
        self.assertEqual(self.form.checkTolerance(100, 99, 0.1, 0.01), Qt.red)
        self.assertEqual(self.form.checkTolerance(100, 70, 0.1, "0.2"), Qt.red)
        
        self.assertRaises(TypeError, self.form.checkTolerance, None, 100)
        self.assertRaises(TypeError, self.form.checkTolerance, 100, None)
        self.assertRaises(TypeError, self.form.checkTolerance, 1, 1, None)
        self.assertRaises(TypeError, self.form.checkTolerance, 1, 1, 1, None)
        self.assertRaises(TypeError, self.form.checkTolerance, "a", 1)
        self.assertRaises(TypeError, self.form.checkTolerance, 1, "a")
        self.assertRaises(TypeError, self.form.checkTolerance, 1, 1, "a")
        self.assertRaises(TypeError, self.form.checkTolerance, 1, 1, 1, "a")
        

    # ������-�� ���������� �������� Visual Studio, ������ �� ��� � �������
#    def testCalcCRC(self):
#        self.assertEqual(

#                , 'A5')
#        self.assertEqual(
#                self.form.calcCRC(':1007E0000A00B30014000E011E00270042004F00')
#                , '53')
