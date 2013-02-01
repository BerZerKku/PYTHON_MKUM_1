# -*- coding: cp1251 -*-
'''
Created on 28.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
# from PyQt4 import QtCore
from PyQt4.QtCore import Qt
# from PyQt4 import Qt


class articleValidate(QtGui.QItemDelegate):
    '''    ������ ���������� ��������
    
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
                if j != 0:
                    # ��� ������/�������������� �������� ������ 0-�� �������
#                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                    # ������ ��������� ������
                    # Qt.ItemIsSelectable
                    # Qt.ItemIsEnabled
                    # Qt.ItemIsEditable
                    flag = Qt.ItemFlags()
                else:
                    flag = Qt.ItemFlags(Qt.ItemIsEnabled)

                item.setFlags(flag)
                self.setItem(i, j, item)
        
        self.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem())
        
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

    # �������� ������������ ����
    def contextMenuEvent(self, event):
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

    def clearTable(self):
        ''' (self) -> None
        
            ������� ��� �������.
        '''
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                
    def delRow(self):
        ''' (self) -> None
        
            ������� ������� ������.
        '''
        i = self.currentRow()
        
        # ������� ����������� ������ ����
        for x in range(i, self.rowCount() - 1):
            for j in range(self.columnCount()):
                self.item(x, j).setText(self.item(x + 1, j).text())
        # ������� ��������� ������
        x = self.rowCount() - 1
        for j in range(self.columnCount()):
            self.item(x, j).setText("")
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MySpreadsheet(3, 3)
    my_frame.show()
    
    my_frame.horizontalHeaderItem(0).setText(u"U���, �")
    my_frame.horizontalHeaderItem(1).setText(u"U���")
    my_frame.horizontalHeaderItem(2).setText(u"I���")
    
    app.exec_()
