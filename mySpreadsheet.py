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
    '''    Пример реализации делегата
        На данный момент не используется.
    
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
        
        # добавим нужное кол-во элементов
        self.setRowCount(row)
        self.setColumnCount(column)
        
#        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
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
                item.setTextAlignment(Qt.AlignCenter)
#                if j != 0:
#                    # для выбора/редактирования доступна только 0-ая колонка
# #                    item.setFlags(QtCore.Qt.ItemIsSelectable)
#                    # пример установки флагов
#                    # Qt.ItemIsSelectable
#                    # Qt.ItemIsEnabled
#                    # Qt.ItemIsEditable
#                    flag = Qt.ItemFlags()
#                else:
#                    flag = Qt.ItemFlags(Qt.ItemIsEnabled)
                 
                # ячейка доступна для выбора
                flag = Qt.ItemFlags(Qt.ItemIsEnabled)
                item.setFlags(flag)
                self.setItem(i, j, item)
        
        self.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem())
        self.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem())
        
        # запретим изменение размеров столбцов и колонок
        # self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        # self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
        # подгонка ширины колонок / строк под размеры таблицы
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        
        # установим ширину колонов в зависимости от размеров окна
#        width_column = size.width() - self.verticalHeader().width()
#        width_column = (width_column - 2) / column
#        for i in range(column):
#            self.setColumnWidth(i, width_column)
        
        # установим высоту колонок в зависимости от размеров окна
#        height_row = size.height() - self.horizontalHeader().height()
#        height_row = (height_row - 2) / row
#        for i in range(row):
#            self.setRowHeight(i, height_row)
        
        # установим запрет на появление скролл-баров
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # запретим изменение размеров таблицы
#        self.setFixedSize(size)

    def contextMenuEvent(self, event):
        ''' (self, event) -> None
            
            Создание контекстного меню, при нажатии RMB на таблице
        '''
        menu = QtGui.QMenu(self)
        
        action1 = QtGui.QAction(u"Удалить строку", self)
        action1.triggered.connect(self.delRow)
        
        action2 = QtGui.QAction(u"Очистить все", self)
        action2.triggered.connect(self.clearTable)
        
        menu.addAction(action1)
        menu.addAction(action2)
        menu.exec_(event.globalPos())
        
    def focusOutEvent(self, event):
        ''' (self, QtGui.QFocusEvent) -> None
        
            Переопределение события потери фокуса виджетом.
        '''
        self.clearSelection()

    def clearTable(self):
        ''' (self) -> None
        
            Очищаем всю таблицу.
        '''
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
        
        self._numFilledRows = 0
                
    def delRow(self):
        ''' (self) -> None
        
            Удаляем текущую строку.
        '''
        i = self.currentRow()
        
        # если это была заполненная строка , удалим ее
        # иначе проигнорируем
        if len(self.item(i, 0).text()) == 0:
            return
        
        # сдвинем вышележащие строки вниз
        for x in range(i, self.rowCount() - 1):
            for j in range(self.columnCount()):
                self.item(x, j).setText(self.item(x + 1, j).text())
        # очистим последнюю строку
        x = self.rowCount() - 1
        for j in range(self.columnCount()):
            self.item(x, j).setText("")
    
    def addRowData(self, data):
        ''' (self, list) -> None
            
            Добавляет строку данных в таблицу и одновременно сортирует ее.
            Кол-во элементов в data должно соответствовать кол-ву столбцов.
            
            При заполнении таблицы устанавливается флаг.
        '''
        
        # возврат, если таблица заполнена
        if self.isFull():
            return

        # добавим строку в конец
        row = self.numFilledRows() - 1
        for col in range(self.columnCount()):
            self.item(row, col).setText(str(data[col]))
            
        # отсортируем данные
        self.sortRows()
        
    def isFull(self):
        ''' (self) -> bool
        
            Возвращает True, в случае полностью зааполненной таблицы.
        '''
        
        # нам достаточно проверить последнюю строку
        return len(self.item(self.rowCount() - 1, 0).text()) != 0
    
    def sortRows(self):
        ''' (self) -> None
        
            Сортировка данным в таблице по возрастанию в первой колонке.
        '''
        print "Сортировка"
        self.sortByColumn(0)
        self.so
#        # нахождение наименьшего индекса пустой строки
#        numRows = self.numFilledRows()
#        for i in range(numRows):
#            max = int(self.item(i, 0).text())
#            for j in range(1, numRows):
#                val = 
            
            
    def numFilledRows(self):
        ''' (self) -> int
        
            Возвращает кол-во заполненых строк в таблице.
        '''
        num = self.rowCount() - 1
        for i in range(self.columnCount()):
            if len(self.item(i, 0).text()) == 0:
                num = i + 1
        
        return num
        
        
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MySpreadsheet(3, 3)
    my_frame.show()
    
    my_frame.horizontalHeaderItem(0).setText(u"Uвых, В")
    my_frame.horizontalHeaderItem(1).setText(u"Uацп")
    my_frame.horizontalHeaderItem(2).setText(u"Iацп")
    
    app.exec_()
