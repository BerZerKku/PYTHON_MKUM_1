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
        
        # сбросим активную ячейку
        self.setCurrentCell(-1, -1)
        
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
        
        for j in range(column):
            self.setHorizontalHeaderItem(j, QtGui.QTableWidgetItem())
        
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
        # запомним текущую строку
        self._row = self.currentRow()
        
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
        self.setCurrentCell(-1, -1)
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")

    def focusInEvent(self, event):
        ''' (self, QtGui.QFocusEvent) -> None
        
            Переопределение события установки фокуса на виджет.
        '''
#        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
    
    def clearTable(self):
        ''' (self) -> None
        
            Очищаем всю таблицу.
        '''
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.item(i, j).setText("")
                
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
                
    def delRow(self):
        ''' (self) -> None
        
            Удаляем текущую строку.
        '''
        # если это была заполненная строка , удалим ее
        # иначе проигнорируем
        if len(self.item(self._row, 0).text()) == 0:
            return
        
        # сдвинем вышележащие строки вниз
        for x in range(self._row, self.rowCount() - 1):
            for j in range(self.columnCount()):
                self.item(x, j).setText(self.item(x + 1, j).text())
                
        # очистим последнюю строку
        x = self.rowCount() - 1
        for j in range(self.columnCount()):
            self.item(x, j).setText("")
            
        self.emit(QtCore.SIGNAL('changeData(QString)'), "")
    
    def addRowData(self, data):
        ''' (self, list) -> None
            
            Добавляет строку данных в таблицу и одновременно сортирует ее,
            по первой колонке. Кол-во элементов в data должно соответствовать
            кол-ву столбцов. Если такой элемент уже есть (совпадение по первой
            колонке), осуществляется замена данных.
        '''
        
        # возврат, если таблица заполнена
        if self.isFull():
            return
        
        numRows = self.numFilledRows()
        val = str(data[0])
        # если подобное значение уже есть в таблице, заменим новыми данными
        # иначе добавим в конец
        for row in range(numRows):
            if val == self.item(row, 0).text():
                numRows = row
                break
        else:
            for col in range(self.columnCount()):
                self.item(numRows, col).setText(str(data[col]))
            
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
        # если кол-во заполненных строк меньше 2 то сортировка не нужна
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
        
            Возвращает кол-во заполненых строк в таблице.
        '''
        
        # просто перебираем строки и проверяем размер текста в 0-ой колонке
        num = 0
        for i in range(self.rowCount()):
            if len(self.item(i, 0).text()) != 0:
                num += 1
        
        return num
    
    def swapRows(self, row1, row2):
        ''' (self, int, int) -> None
        
            Меняет местами две строки.
        '''
        for col in range(self.columnCount()):
            tmp = self.item(row1, col).text()
            self.item(row1, col).setText(self.item(row2, col).text())
            self.item(row2, col).setText(tmp)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MySpreadsheet(row=3, column=3)
    my_frame.show()
    
    my_frame.horizontalHeaderItem(0).setText(u"Uвых, В")
    my_frame.horizontalHeaderItem(1).setText(u"Uацп")
    my_frame.horizontalHeaderItem(2).setText(u"Iацп")
    
    app.exec_()
