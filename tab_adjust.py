# -*- coding: cp1251 -*-
'''
Created on 20.12.2012

@author: Shcheblykin
'''

import sys
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


class TabAdjust(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        hbox = QtGui.QHBoxLayout(self)
        grid = QtGui.QGridLayout()
        self.adjTable = mySpreadsheet.MySpreadsheet()
        self.adjTable.horizontalHeaderItem(0).setText(u"U���, �")
        self.adjTable.horizontalHeaderItem(1).setText(u"U���")
        self.adjTable.horizontalHeaderItem(2).setText(u"I���")
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
        self.entValU = QtGui.QLineEdit(u'U���')
        self.entValU.setValidator(QtGui.QIntValidator(1, 100, self))
        self.entValU.clear()  # ������� ������
        #    ������ ����������� ����, �.�. ����� ���� �������� � 'Undo'
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.entValU.textChanged.connect(self.valUChange)
          
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
        
#        self.readValI2 = QtGui.QLineEdit(u'��� ������')
#        self.readValI2.setDisabled(True)
# #        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValI2 = QtGui.QCheckBox()
#        self.checkValI2.setChecked(False)
#        self.checkValI2.setDisabled(True)
#        self.checkValI2.setToolTip(u"���./����. ���������� ���������.")
#        
#        self.readValU48 = QtGui.QLineEdit(u'��� ������')
#        self.readValU48.setDisabled(True)
# #        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValU48 = QtGui.QCheckBox()
#        self.checkValU48.setChecked(False)
#        self.checkValU48.setDisabled(True)
#        self.checkValU48.setToolTip(u"���./����. ���������� ���������.")
#        
#        self.readValUwork = QtGui.QLineEdit(u'��� ������')
#        self.readValUwork.setDisabled(True)
# #        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValUwork = QtGui.QCheckBox()
#        self.checkValUwork.setChecked(False)
#        self.checkValUwork.setDisabled(True)
#        self.checkValUwork.setToolTip(u"���./����. ���������� ���������.")
        
        self.pSave = QtGui.QPushButton(u'���������')
        self.pSave.clicked.connect(self.saveFileHEX)
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
        grid.addLayout(hbox1, 7, 0, 2, 1)
        
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
        
#        #     ��� ������ 2
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'��� ������ 2'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValI2, row, col + 1)
#        grid.addWidget(self.checkValI2, row, col + 2)

#        #     ���������� �������
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'���������� �������'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValU48, row, col + 1)
#        grid.addWidget(self.checkValU48, row, col + 2)

#        #     ���������� � ������� �����
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'���������� ���.�'), row, col,
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
        valUout = self.entValU.text()
        self.entValU.setText("")
        
        valU = 0
        if self.checkValU.isChecked():
            flag, valU = self.checkValue(self.readValU.text())
            if not flag:
                print u'������ �������� ��� "��������� ������"'
                error = True
        
        valI1 = 0
        if self.checkValI1.isChecked():
            flag, valI1 = self.checkValue(self.readValI1.text())
            if not flag:
                print u'������ �������� ��� "��� ������ 1"'
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
            return
        
        # ������� ������, � ������� ���� �����
        data = [valUout, valU, valI1]
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
            print self, u'������ �������������� ������ � int'
            val = 0
        
        return sost, val
    
    def openFile(self):
        ''' (self) -> None
            
            �������� ����� �������� � ����������� ����������� �������.
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, u'�������',
                                                    filter="HEX Files (*.hex)")
        
        try:
            fileHEX = open(filename, 'r')
            origHEX = fileHEX.read()
            fileHEX.close()
            origHEX = origHEX.splitlines()
        except:
            print u"�� ������� ������� ���� ��������."
            return
        
        # ����� ������ ��������� ������
        posLine = 0
        posInData = -1
        for i in range(len(origHEX)):
            # -9 - ��������� ����������
            posInData = origHEX[i].find("9178") - 9
            if posInData >= 0:
                posLine = i
                break
        else:
            print u"������ ����� ��������"
            return
        
        # 4 ����� - '9178'
        # 8 ���� - ��������� ��� ���������� � ������� �����
        # 8 ���� - ��������� ��� ���������� �������
        # 4 * (16) - ������ ������ int(U���, u, I���, i)
        lenght = 4 + 8 + 8 + 4 * (4 + 4 + 4 + 4)
        l = 0
        
        # ���������� ������ ������
        m = ""
        while l < lenght:
#            print "old = ", origHEX[posLine]
            data = origHEX[posLine][9 + posInData:-2]
            # ���������� �� ������������ ��� 20 ������ ��������
            s = ""
            for char in data:
                if l >= 20:
                    s += char
                l += 1
            m += s
            posLine += 1
            posInData = 0
        
        # �������� ������ �� int
        mas = []
        for i in range(16):
            tmp = m[i * 4: i * 4 + 4]
            tmp = tmp[-2:] + tmp[:2]
            mas.append(int(tmp, 16))
        # ���������� �������
        for row in range(4):
            self.adjTable.item(row, 0).setText(str(mas[row * 2 + 1]))
            self.adjTable.item(row, 1).setText(str(mas[row * 2 + 0]))
            self.adjTable.item(row, 2).setText(str(mas[row * 2 + 8]))
        
    def openFileHEX(self):
        ''' (self) -> str
        
            �������� ����� ��������. ���������� ���������� �����.
        '''
        fileHEX = open('MkUM.dat', 'r')
        text = fileHEX.read()
        fileHEX.close()

        return text
    
    def saveFileAs(self):
        ''' (self) -> None
            
            ���������� ����� � ������� ������� "��������� ���...".
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, u"��������� ���...",
                                        filter="HEX Files (*.hex)")
        if filename:
            self.saveFileHEX(name=filename)
    
    def saveFileHEX(self, chacked=False, name='MkUM.hex'):
        ''' (self, name) -> None
            
            ��������� ���� �������� � �����/������� name
            chacked - 
        '''
        # ������� ���� �������� � �������� �� �� ������
        try:
            origHEX = self.openFileHEX()
            origHEX = origHEX.splitlines()
        except:
            print u"�� ������� ������� ������������ ���� ��������."
            return
        
        # ������� �� ������� ��������, � ����������� �� � hex-������
        data = ""
        #    ����������
        for row in range(4):
            tmp = self.intToHex(self.adjTable.item(row, 1).text())
            tmp += self.intToHex(self.adjTable.item(row, 0).text())
            data += tmp
        #    ���
        for row in range(4):
            tmp = self.intToHex(self.adjTable.item(row, 2).text())
            i = int(round(int(self.adjTable.item(row, 0).text()) * 1000 / 75.0))
            tmp += self.intToHex(str(i))
            data += tmp
            
        # ����� ������ ��������� ������
        posLine = 0
        posInData = -1
        for i in range(len(origHEX)):
            # -9 - ��������� ����������
            posInData = origHEX[i].find("9178") - 9
            if posInData >= 0:
                # 20 - "9178" + 2 float �������������
                posInData += 20
                posLine = i
                break
        else:
            print u"������ ��������� ����� ��������"
            return
    
        # �������� hex-file
        # � ������ ������ ������� 9 ���� - ��������� ����������
        # ����� � ������ ������
        # 1      ":" - ������� ������ ������
        # 2-3    "xx" - ���-�� ���� ������ � ���� ������
        # 4-7    "xxyy" - �����
        # 8-9    "00" - ������ ��������� �����
        # 10-13  "9178" - ������ �������
        # 14-21  "aabbccdd" - ��������� ��� ���������� � ���.����� (float)
        # 22-29  "aabbccdd" - ��������� ��� ���������� ������� (float)
        # 30-33  "aabb" - ������ ����������, ������� ������ ������ (int)
        # 34-37  "aabb" - ������ �������� ���, ������� ������ ������ (int)
        # 38-41  "aabb" - ������ ����������, ������� ������ ������ (int)
        while len(data) > 0:
#            print "old = ", origHEX[posLine]
            infoInLine = origHEX[posLine][:9]
            bytesInLine = int(origHEX[posLine][1:3], 16)
            # dataInLine = origHEX[posLine][9:9 + 2 * bytesInLine]
            tmp = data[:bytesInLine * 2 - posInData]
#            print "posInData = %d, bytesInLine = %d" % (posInData,bytesInLine)
#            print "tmp = %s, len = %d" % (tmp, len(tmp) / 2)
            data = data.replace(tmp, "")
            # ��� �������������, ������ ������ ������������� �������
            if len(data) == 0:
                tmp += origHEX[posLine][bytesInLine * 2 - posInData - 3:-2]
#            print "data = %s, len = %d" % (data, len(data) / 2)
            newDataInLine = origHEX[posLine][9:9 + posInData] + tmp
            origHEX[posLine] = infoInLine + newDataInLine
            origHEX[posLine] += self.calcCRC(origHEX[posLine])
#            print "new = ", origHEX[posLine]
            posLine += 1
            posInData = 0
    
        fSave = open(name, 'w')
        for x in origHEX:
            fSave.write(x + '\n')
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
        
    def debugSaveFile(self, data):
        ''' (self) -> None
        
            ���������� ����� ��� �������.
        '''
        for i in range(self.adjTable.rowCount()):
            self.adjTable.item(i, 0).setText(str(data[0][i * 2 + 1]))
            self.adjTable.item(i, 1).setText(str(data[0][i * 2]))
            self.adjTable.item(i, 2).setText(str(data[1][i * 2]))
        
        self.pSave.setEnabled(True)
        self.pSaveAs.setEnabled(True)
            
            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabAdjust()
    my_frame.show()
    
    # data 1
    # my_frame.debugSaveFile([[43, 5, 88, 10, 179, 20, 270, 30],
    #                        [39, 66, 79, 133, 159, 266, 242, 400]])
    my_frame.debugSaveFile([[40, 5, 81, 10, 172, 20, 263, 30],
                            [45, 66, 90, 133, 187, 266, 283, 400]])
    
    # ��������� ��� �����������
    QtGui.QApplication.setStyle('Cleanlooks')
    
    app.exec_()
