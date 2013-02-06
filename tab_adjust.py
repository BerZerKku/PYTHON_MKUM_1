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
        self.adjTable.horizontalHeaderItem(0).setText(u"Uвых, В")
        self.adjTable.horizontalHeaderItem(1).setText(u"Uацп")
        self.adjTable.horizontalHeaderItem(2).setText(u"Iацп")
        self.adjTable.clearTable()
        self.connect(self.adjTable, QtCore.SIGNAL('changeData(QString)'),
                     self.valUChange)
        
        self.pAdd = QtGui.QPushButton(u'Добавить')
        self.pAdd.setDisabled(True)
        self.pAdd.clicked.connect(self.addPointToTable)
        
#        self.pDel = QtGui.QPushButton(u'Удалить')
        
        # для всех LineEdit отключим контекстное меню
        # .setContextMenuPolicy(Qt.NoContextMenu)
        
        # создадим поле для ввоода значения напряжения
        # это должно быть целое число от 1 до 100В
        self.entValU = QtGui.QLineEdit(u'Uвых')
        self.entValU.setValidator(QtGui.QIntValidator(1, 100, self))
        self.entValU.clear()  # очистка текста
        #    уберем контекстное меню, т.к. могут быть проблемы с 'Undo'
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.entValU.textChanged.connect(self.valUChange)
          
        self.readValU = QtGui.QLineEdit(u'Нет данных')
        self.readValU.setDisabled(True)
#        self.readValU.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValU = QtGui.QCheckBox()
        self.checkValU.setChecked(True)
        self.checkValU.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.readValI1 = QtGui.QLineEdit(u'Нет данных')
        self.readValI1.setDisabled(True)
#        self.readValI1.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValI1 = QtGui.QCheckBox()
        self.checkValI1.setChecked(True)
        self.checkValI1.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.readValI2 = QtGui.QLineEdit(u'Нет данных')
        self.readValI2.setDisabled(True)
#        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValI2 = QtGui.QCheckBox()
        self.checkValI2.setChecked(False)
        self.checkValI2.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.readValU48 = QtGui.QLineEdit(u'Нет данных')
        self.readValU48.setDisabled(True)
#        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValU48 = QtGui.QCheckBox()
        self.checkValU48.setChecked(False)
        self.checkValU48.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.readValUwork = QtGui.QLineEdit(u'Нет данных')
        self.readValUwork.setDisabled(True)
#        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValUwork = QtGui.QCheckBox()
        self.checkValUwork.setChecked(False)
        self.checkValUwork.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.saveFileHEX)
        self.pSave.setDisabled(True)
        
        self.pSaveAs = QtGui.QPushButton(u'Сохранить как...')
        self.pSaveAs.setDisabled(True)
        
        # создаем область для графика
#        self.figure = pylab.figure()
#        self.canvas = FigureCanvas(self.figure)
#        self.canvas.setFixedSize(400, 400)
#        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
#        self.axes.set_title('Haba-haba')
        
        # установка таблицы в сетку
        grid.addWidget(self.adjTable, 0, 0, 7, 2)
        
        grid.addWidget(self.pSave, 7, 0)
        grid.addWidget(self.pSaveAs, 7, 1)
        
        # начальные положения для полей данных
        col = 2
        row = 0
        
        # входное напряжение
        grid.addWidget(QtGui.QLabel(u'Напряжение выхода, В'), row, col, 1, 2,
                       Qt.AlignCenter)
        row += 1
        grid.addWidget(self.entValU, row, col)
        grid.addWidget(self.pAdd, row, col + 1)
        
        # показания АЦП
        row += 1
        grid.addWidget(QtGui.QLabel(u'Показания АЦП'), row, col, 1, 2,
                       Qt.AlignCenter)
        
        #     напряжение выхода
        row += 1
        grid.addWidget(QtGui.QLabel(u'Напряжение выхода'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU, row, col + 1)
        grid.addWidget(self.checkValU, row, col + 2)
        
        #     ток выхода 1
        row += 1
        grid.addWidget(QtGui.QLabel(u'Ток выхода 1'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI1, row, col + 1)
        grid.addWidget(self.checkValI1, row, col + 2)
        
        #     ток выхода 2
        row += 1
        grid.addWidget(QtGui.QLabel(u'Ток выхода 2'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI2, row, col + 1)
        grid.addWidget(self.checkValI2, row, col + 2)
        
        #     напряжение питания
        row += 1
        grid.addWidget(QtGui.QLabel(u'Напряжение питания'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU48, row, col + 1)
        grid.addWidget(self.checkValU48, row, col + 2)
        
        #     напряжение в рабочей точке
        row += 1
        grid.addWidget(QtGui.QLabel(u'Напряжение раб.т'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValUwork, row, col + 1)
        grid.addWidget(self.checkValUwork, row, col + 2)
        
        hbox.addLayout(grid)
#        hbox.addWidget(self.canvas)
        
        # каждые 200мс будет проверять возможность ввода новго значения
#        self.timer = QtCore.QTimer()
#        self.timer.start(200)
#        self.timer.timeout.connect(self.valUChange)
        
    def addPointToTable(self):
        ''' (self) -> None [SLOT]
            
            Добавление новой записи в таблицу данных
        '''
        
        # флаг состояния
        error = False
        
        # считаем и проверим имеющиеся данные
        # если по окончанию проверки флаг error будет True
        # добавление строки не произойдет
        valUout = self.entValU.text()
        self.entValU.setText("")
        
        valU = 0
        if self.checkValU.isChecked():
            flag, valU = self.checkValue(self.readValU.text())
            if not flag:
                print u'Ошибка значения АЦП "Напряжени выхода"'
                error = True
        
        valI1 = 0
        if self.checkValI1.isChecked():
            flag, valI1 = self.checkValue(self.readValI1.text())
            if not flag:
                print u'Ошибка значения АЦП "Ток выхода 1"'
                error = True
        
        valI2 = 0
        if self.checkValI2.isChecked():
            flag, valI2 = self.checkValue(self.readValI2.text())
            if not flag:
                print u'Ошибка значения АЦП "Ток выхода 2"'
                error = True
        
        valU48 = 0
        if self.checkValU48.isChecked():
            flag, valU48 = self.checkValue(self.readValU48.text())
            if not flag:
                print u'Ошибка значения АЦП "Напряжение питания"'
                error = True
        
        valUwork = 0
        if self.checkValUwork.isChecked():
            flag, valUwork = self.checkValue(self.readValUwork.text())
            if not flag:
                print u'Ошибка значения АЦП "Напряжение рабочей точки"'
                error = True
        
        # если была ошибка
        if error:
            return
        
        # добавим строку, и очистим поле ввода
        data = [valUout, valU, valI1]
        self.adjTable.addRowData(data)
        
        if self.adjTable.isFull():
            self.pAdd.setDisabled(True)
                   
    def valUChange(self, val=""):
        ''' (self, str) -> None
        
            Реакция на ввод/изменение напряжения. При отсутствии текста в поле
            блокируется возможность добавления новой записи. При заполненной
            таблице, появляется возможность сохранить прошивку.
        '''

        val = self.entValU.text()
        if self.adjTable.isFull():
            # таблица полная, запретим возможность добавления данных
            # и разрешим сохранение прошивки
            self.pAdd.setDisabled(True)
            self.pSave.setEnabled(True)
            self.pSaveAs.setEnabled(True)
        else:
            # таблица не полная, запретим возможность сохранения прошивики
            # и проверим данные в поле ввода напряжения
            self.pSave.setDisabled(True)
            self.pSaveAs.setDisabled(True)
            if len(val) == 0:
                self.pAdd.setDisabled(True)
            else:
                self.pAdd.setEnabled(True)
            
    def checkValue(self, text):
        ''' (self, str) -> bool, int
        
            Входная строка преобразуется в число val. Если полученное значение
            выходит за диапазон 0..1023, возвращается False, val.
            Иначе True, val.
        '''
        
        sost = False
        
        try:
            val = int(text)
        
            if val >= 0 and val <= 1023:
                sost = True
        except:
            print self, u'Ошибка преобразования строки в int'
            val = 0
        
        return sost, val
    
    def openFileHEX(self):
        ''' (self) -> str
        
            Открытие файла прошивки. Возвращает содержимое файла.
        '''
        fileHEX = open('MkUM.hex', 'r')
        text = fileHEX.read()

        return text
    
    def saveFileHEX(self, name):
        ''' (self, name) -> None
            
            Сохраняем файл прошивки с путем/имененм name
        '''
        # считаем файл прошивки и разобъем ее на строки
        try:
            origHEX = self.openFileHEX()
            origHEX = origHEX.splitlines()
        except:
            print u"Не удалось считать оригинальный файл прошивки."
            return
        
        # поиск начала структуры данных
        numLine = 0
        for i in range(len(origHEX)):
            if "9178" in origHEX[i]:
                numLine = i
                print origHEX[i]
                break
        else:
            print u"Ошибка исходного файла прошивки"
            return
        
        # считаем из таблицы значения, и преобразуем их в hex-строку 
        data = ""
        for row in range(4):
            for col in range(2):
                data += self.intToHex(self.adjTable.item(row, col).text())
        print data
        
        
        # байты в первой строке
        # 1      ":" - признак начала строки
        # 2-3    "xx" - кол-во байт данных в этой строке
        # 4-7    "xxyy" - адрес 
        # 8-9    "00" - данные двоичного файлы
        # 10-13  "9178" - начало массива
        # 14-21  "aabbccdd" - множитель для напряжения в раб.точке (float)
        # 22-29  "aabbccdd" - множитель для напряжения питания (float)
        # 30-33  "aabb" - первое напряжение, младшим байтом вперед (int)
        # 34-37  "aabb" - первое значение АЦП, младшим байтом вперед (int)
        # 38-41  "aabb" - второе напряжение, младшим байтом вперед (int)
        
        
        
        
    def intToHex(self, val):
        ''' (self, int) -> str
        
            Преобразование int в строку hex. Младшим байтом вперед.
            
            >>> .intToHex(5) 
            '0500'
            >>> .intToHex(270)
            '0E01'
        '''
        # преобразование int в строку
        val = '%.4x' % int(val)
        val = val.upper()
        # разделение строки на старший и младший "байты"
        hi = val[:2]
        low = val[2:]
        # склейка новой строки, младшим байтом вперед
        val = low + hi
        
        return val
        
            
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = TabAdjust()
    my_frame.show()
    
    # my_frame.saveFileHEX('a')
    
    # установим вид отображения
    QtGui.QApplication.setStyle('Cleanlooks')
    
    
    app.exec_()
