# -*- coding: cp1251 -*-
'''
Created on 28.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class articleValidate(QtGui.QItemDelegate):
    '''    Пример реализации делегата
    
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
        pass


class MySpreadsheet(QtGui.QTableWidget):
    def __init__(self, row=4, column=3, size=QtCore.QSize(100, 100),
                 parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        
        # добавим нужное кол-во элементов
        self.setRowCount(row)
        self.setColumnCount(column)
        
        # Пример использования своего делегата
#        myDeligate = articleValidate()
#        self.setItemDelegateForColumn(1, myDeligate)
#        self.setItemDelegateForColumn(2, myDeligate)
        
        # Изменение способов выбора ячеек и воздействия на них
#        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
#        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
                
        # заполнение таблицы
        for i in range(row):
            for j in range(column):
                item = QtGui.QTableWidgetItem("R%d C%d" % (i, j))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if j != 0:
                    # для выбора/редактирования доступна только 0-ая колонка
#                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                    # пример установки флагов
#                   flag = QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsSelectable |
#                                              QtCore.Qt.ItemIsEnabled |
#                                              QtCore.Qt.ItemIsEditable)
                    item.setFlags(QtCore.Qt.ItemFlags())
                self.setItem(i, j, item)
        
        self.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem())
        
        # запретим изменение размеров столбцов и колонок
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
        # установим ширину колонов в зависимости от размеров окна
        width_column = size.width() - self.verticalHeader().width()
        width_column = (width_column - 2) / column
        for i in range(column):
            self.setColumnWidth(i, width_column)
        
        # установим высоту колонок в зависимости от размеров окна
        height_row = size.height() - self.horizontalHeader().height()
        height_row = (height_row - 2) / row
        for i in range(row):
            self.setRowHeight(i, height_row)
        
        # установим запрет на появление скролл-баров
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # запретим изменение размеров таблицы
        self.setFixedSize(size)
                
    def focusOutEvent(self, event):
        ''' (self, QtGui.QFocusEvent) -> None
        
            Переопределение события потери фокуса виджетом.
        '''
        self.clearSelection()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MySpreadsheet(20, 20, QtCore.QSize(500, 500))
    my_frame.show()
    
    my_frame.horizontalHeaderItem(0).setText(u"Uвых, В")
    my_frame.horizontalHeaderItem(1).setText(u"Uацп")
    my_frame.horizontalHeaderItem(2).setText(u"Iацп")
    
    app.exec_()
