# -*- coding: cp1251 -*-
'''
Created on 28.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
# from PyQt4 import Qt


class articleValidate(QtGui.QItemDelegate):
    '''    ������ ���������� ��������
        �� ������ ������ �� ������������.
    
    '''
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, options, index):
        print self
        print parent
        print options
        print index.row()
        print index.column()
        
    def drawFocus(self, parent, options, rec):
        print 'haba haba'
        
    def setEditTriggers(self):
        print 'ggg'
        pass
    

class MySpreadsheet(QtGui.QTableWidget):
    def __init__(self, row=4, column=3, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
        # ������� ������ ���-�� ���������
        self.setRowCount(row)
        self.setColumnCount(column)
        
        # ������� �������� ������
        self.setCurrentCell(-1, -1)
        
#        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # ������ ������������� ������ ��������
#        myDeligate = articleValidate()
#        self.setItemDelegateForColumn(1, myDeligate)
#        self.setItemDelegateForColumn(2, myDeligate)
        
        # ��������� �������� ������ ����� � ����������� �� ���
#        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
#        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
                
        # ���������� �������
        for i in range(row):
            for j in range(column):
                
                item = QtGui.QTableWidgetItem("R%d C%d" % (i, j))
                item.setTextAlignment(Qt.AlignCenter)
#                if j != 0:
#                    # ��� ������/�������������� �������� ������ 0-�� �������
# #                    item.setFlags(QtCore.Qt.ItemIsSelectable)
#                    # ������ ��������� ������
#                    # Qt.ItemIsSelectable
#                    # Qt.ItemIsEnabled
#                    # Qt.ItemIsEditable
#                    flag = Qt.ItemFlags()
#                else:
#                    flag = Qt.ItemFlags(Qt.ItemIsEnabled)
                 
                # ������ �������� ��� ������
                flag = Qt.ItemFlags(Qt.ItemIsEnabled)
                item.setFlags(flag)
                self.setItem(i, j, item)
        
        for j in range(column):
            self.setHorizontalHeaderItem(j, QtGui.QTableWidgetItem())
        
        # �������� ��������� �������� �������� � �������
        # self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        # self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
        # �������� ������ ������� / ����� ��� ������� �������
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        
        # ��������� ������ ������� � ����������� �� �������� ����
#        width_column = size.width() - self.verticalHeader().width()
#        width_column = (width_column - 2) / column
#        for i in range(column):
#            self.setColumnWidth(i, width_column)
        
        # ��������� ������ ������� � ����������� �� �������� ����
#        height_row = size.height() - self.horizontalHeader().height()
#        height_row = (height_row - 2) / row
#        for i in range(row):
#            self.setRowHeight(i, height_row)
        
        # ��������� ������ �� ��������� ������-�����
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # �������� ��������� �������� �������
#        self.setFixedSize(size)

    def contextMenuEvent(self, event):
        ''' (self, event) -> None
            
            �������� ������������ ����, ��� ������� RMB �� �������
        '''
        # �������� ������� ������
        self._row = self.currentRow()
        
        menu = QtGui.QMenu(self)
        
        action1 = QtGui.QAction(u"������� ������", self)
        action1.triggered.connect(self.delRow)
        
        action2 = QtGui.QAction(u"�������� ���", self)
        action2.triggered.connect(self.clearTable)
        
        menu.addAction(action1)
        menu.addAction(action2)
        menu.exec_(event.globalPos())
        
    def focusOutEvent(self, event):
        ''' (self, QtGui.QFocusEvent) -> None
        
            ��������������� ������� ������ ������ ��������.
        '''
        self.clearSelection()
        self.setCurrentCell(-1, -1)
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")

    def focusInEvent(self, event):
        ''' (self, QtGui.QFocusEvent) -> None
        
            ��������������� ������� ��������� ������ �� ������.
        '''
#        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
    
    def clearTable(self):
        ''' (self) -> None
        
            ������� ��� �������.
        '''
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
                
    def delRow(self):
        ''' (self) -> None
        
            ������� ������� ������.
        '''
        # ���� ��� ���� ����������� ������ , ������ ��
        # ����� �������������
        if len(self.item(self._row, 0).text()) == 0:
            return
        
        # ������� ����������� ������ ����
        for x in range(self._row, self.rowCount() - 1):
            for j in range(self.columnCount()):
                self.item(x, j).setText(self.item(x + 1, j).text())
                
        # ������� ��������� ������
        x = self.rowCount() - 1
        for j in range(self.columnCount()):
            self.item(x, j).setText("")
            
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
    
    def addRowData(self, data):
        ''' (self, list) -> None
            
            ��������� ������ ������ � ������� � ������������ ��������� ��,
            �� ������ �������. ���-�� ��������� � data ������ ���������������
            ���-�� ��������. ���� ����� ������� ��� ���� (���������� �� ������
            �������), �������������� ������ ������.
        '''
        
        # �������, ���� ������� ���������
        if self.isFull():
            return
        
        numRows = self.numFilledRows()
        val = str(data[0])
        # ���� �������� �������� ��� ���� � �������, ������� ������ �������
        # ����� ������� � �����
        for row in range(numRows):
            if val == self.item(row, 0).text():
                numRows = row
                break
        else:
            for col in range(self.columnCount()):
                self.item(numRows, col).setText(str(data[col]))
            
        # ����������� ������
        self.sortRows()
        
    def isFull(self):
        ''' (self) -> bool
        
            ���������� True, � ������ ��������� ������������ �������.
        '''
        # ��� ���������� ��������� ��������� ������
        return len(self.item(self.rowCount() - 1, 0).text()) != 0
    
    def sortRows(self):
        ''' (self) -> None
        
            ���������� ������ � ������� �� ����������� � ������ �������.
        '''
        # ���� ���-�� ����������� ����� ������ 2 �� ���������� �� �����
        numRows = self.numFilledRows()
        if numRows <= 1:
            return
        
        numRows -= 1
        for j in range(numRows):
            for i in range(numRows - j):
                val_1 = float(self.item(i, 0).text())
                val_2 = float(self.item(i + 1, 0).text())
                if (val_1 > val_2):
                    self.swapRows(i, i + 1)
            
    def numFilledRows(self):
        ''' (self) -> int
        
            ���������� ���-�� ���������� ����� � �������.
        '''
        
        # ������ ���������� ������ � ��������� ������ ������ � 0-�� �������
        num = 0
        for i in range(self.rowCount()):
            if len(self.item(i, 0).text()) != 0:
                num += 1
        
        return num
    
    def swapRows(self, row1, row2):
        ''' (self, int, int) -> None
        
            ������ ������� ��� ������.
        '''
        for col in range(self.columnCount()):
            tmp = self.item(row1, col).text()
            self.item(row1, col).setText(self.item(row2, col).text())
            self.item(row2, col).setText(tmp)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MySpreadsheet(row=3, column=3)
    my_frame.show()
    
    my_frame.horizontalHeaderItem(0).setText(u"U���, �")
    my_frame.horizontalHeaderItem(1).setText(u"U���")
    my_frame.horizontalHeaderItem(2).setText(u"I���")
    
    app.exec_()
