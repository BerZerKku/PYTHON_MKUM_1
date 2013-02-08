# -*- coding: cp1251 -*-
'''
Created on 24.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class SetupCOM(QtGui.QWidget):
    ''' class
    
        Widget ������ � ���-������.
        ������� ����������� ������ ��������� ������ � �������,
        ��������� ���������� ������, �������� � �������� �����.
        ����������/������������ ���-�� ��������� �� �����.
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        # ��������� �������������� ������� ����
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # ���� ������� ���������
        self._modify = False
        
        # �������� ��������� �������
        self.createWidget()

    def fillPortBox(self, data, val='COM1'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ������ ������� data
            �� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        self.portEdit.clear()
        self.portEdit.addItems(data)
        if val in data:
            self.portEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.portEdit.setCurrentIndex(0)
    
    def fillBaudRateBox(self, data, val='19200'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ��������� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        self.baudRateEdit.clear()
        self.baudRateEdit.addItems(data)
        if val in data:
            self.baudRateEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.baudRateEdit.setCurrentIndex(0)
    
    def fillStopBitsBox(self, data, val='2'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ����-����� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        self.stopBitsEdit.clear()
        self.stopBitsEdit.addItems(data)
        if val in data:
            
            self.stopBitsEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.stopBitsEdit.setCurrentIndex(0)
        
    def fillParityBox(self, data, val='None'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ��������� ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        self.parityEdit.clear()
        self.parityEdit.addItems(data)
        if val in data:
            
            self.parityEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.parityEdit.setCurrentIndex(0)
    
    def fillByteSize(self, data, val='8'):
        ''' (self, list, str) -> None
        
            ���������� ��������������� ������ ���-�� ��� ������ ������� data.
            ��� ������� � ������ �������� val, ��� ����� �������.
        '''
        # �������� ��������� ����� ����������� � �� ����� ����������,
        # ���� �� ��� ����������
        tmp = self.isFlagModify()
        
        self.byteSizeEdit.clear()
        self.byteSizeEdit.addItems(data)
        if val in data:
            self.byteSizeEdit.setCurrentIndex(data.index(val))
            if not tmp:
                self.clearFlagModify()
        else:
            self.byteSizeEdit.setCurrentIndex(0)
    
    def setFlagModify(self, val=None):
        ''' (self, val) -> None
            
            ��������� ����� ������� ��������� ����������.
            val - ������ �������������� ��������
        '''
        self._modify = True
        self.pApply.setEnabled(True)
    
    def isFlagModify(self):
        ''' (self) -> None
        
            �������� ������� ��������� ����������.
        '''
        return self._modify
        
    def clearFlagModify(self):
        ''' (self) -> None
            
            ����� ����� ������� ��������� ����������
        '''
        self._modify = False
        self.pApply.setDisabled(True)
    
    def debug(self):
        ''' (self, list) -> None
        
            �������
        '''
        self.portEdit.addItem('COM121')

    def createWidget(self):
        ''' (self, bool) -> None
        
            ������������ ��������� ����.
            debug - �������� �� ����� ������:
                False - ������� (�� ���������)
                True - �������
        '''
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.portEdit = QtGui.QComboBox()
        self.portLabel = QtGui.QLabel(u'���:')
        vboxl.addWidget(self.portLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.portEdit)
        
        self.baudRateEdit = QtGui.QComboBox()
        self.baudRateLabel = QtGui.QLabel(u'�������� ���/�:')
        vboxl.addWidget(self.baudRateLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.baudRateEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        groupbox1 = QtGui.QGroupBox(u'��������')
        groupbox1.setLayout(hbox)
        
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.byteSizeEdit = QtGui.QComboBox()
        self.byteSizeLabel = QtGui.QLabel(u'���� ������:')
        vboxl.addWidget(self.byteSizeLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.byteSizeEdit)
        
        self.parityEdit = QtGui.QComboBox()
        self.parityLabel = QtGui.QLabel(u'��������:')
        vboxl.addWidget(self.parityLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.parityEdit)
        
        self.stopBitsEdit = QtGui.QComboBox()
        self.stopBitsLabel = QtGui.QLabel(u'�������� ����:')
        vboxl.addWidget(self.stopBitsLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.stopBitsEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        
        groupbox2 = QtGui.QGroupBox(u'������ ������')
        groupbox2.setLayout(hbox)
        
        self.pScan = QtGui.QPushButton(u'��������')
        self.connect(self.pScan, QtCore.SIGNAL('clicked()'), self.debug)
        
        self.pApply = QtGui.QPushButton(u'�������')
        self.pAbort = QtGui.QPushButton(u'��������')
        
        vboxl = QtGui.QVBoxLayout()
        vboxl.addWidget(groupbox1)
        vboxl.addWidget(groupbox2)
        
        vboxr = QtGui.QVBoxLayout()
        vboxr.addWidget(self.pApply)
        vboxr.addWidget(self.pScan)
        vboxr.addWidget(self.pAbort)
        vboxr.addStretch()

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxr)
        
        self.setLayout(hbox)
        
        # ��������� �������
        self.portEdit.currentIndexChanged.connect(self.setFlagModify)
        self.baudRateEdit.currentIndexChanged.connect(self.setFlagModify)
        self.byteSizeEdit.currentIndexChanged.connect(self.setFlagModify)
        self.stopBitsEdit.currentIndexChanged.connect(self.setFlagModify)
        self.parityEdit.currentIndexChanged.connect(self.setFlagModify)
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = SetupCOM()
    my_frame.fillPortBox(['COM1', 'COM2', 'COM6'])
    my_frame.fillBaudRateBox(['4800', '9600', '19200'])
    my_frame.fillByteSize(['4', '5', '6', '7', '8'])
    my_frame.fillParityBox(['None', 'Odd', 'Even', 'Mark', 'Space'])
    my_frame.fillStopBitsBox(['1', '1.5', '2'])
    
    my_frame.show()
    app.exec_()
