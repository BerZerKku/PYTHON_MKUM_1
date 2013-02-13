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
        
#        self.readValI2 = QtGui.QLineEdit(u'Нет данных')
#        self.readValI2.setDisabled(True)
# #        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValI2 = QtGui.QCheckBox()
#        self.checkValI2.setChecked(False)
#        self.checkValI2.setDisabled(True)
#        self.checkValI2.setToolTip(u"Вкл./выкл. калибровки параметра.")
#        
#        self.readValU48 = QtGui.QLineEdit(u'Нет данных')
#        self.readValU48.setDisabled(True)
# #        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValU48 = QtGui.QCheckBox()
#        self.checkValU48.setChecked(False)
#        self.checkValU48.setDisabled(True)
#        self.checkValU48.setToolTip(u"Вкл./выкл. калибровки параметра.")
#        
#        self.readValUwork = QtGui.QLineEdit(u'Нет данных')
#        self.readValUwork.setDisabled(True)
# #        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValUwork = QtGui.QCheckBox()
#        self.checkValUwork.setChecked(False)
#        self.checkValUwork.setDisabled(True)
#        self.checkValUwork.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.saveFileHEX)
        self.pSave.setDisabled(True)
        
        self.pSaveAs = QtGui.QPushButton(u'Сохранить как...')
        self.pSaveAs.clicked.connect(self.saveFileAs)
        self.pSaveAs.setDisabled(True)
        
        self.pOpen = QtGui.QPushButton(u'Открыть...')
        self.pOpen.clicked.connect(self.openFile)
        self.pOpen.setEnabled(True)
        
        # создаем область для графика
#        self.figure = pylab.figure()
#        self.canvas = FigureCanvas(self.figure)
#        self.canvas.setFixedSize(400, 400)
#        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
#        self.axes.set_title('Haba-haba')
        
        # установка таблицы в сетку
        grid.addWidget(self.adjTable, 0, 0, 7, 2)
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.pOpen)
        hbox1.addWidget(self.pSave)
        hbox1.addWidget(self.pSaveAs)
#        grid.addWidget(self.pSave, 7, 0)
#        grid.addWidget(self.pSaveAs, 7, 1)
        grid.addLayout(hbox1, 7, 0, 2, 1)
        
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
        
#        #     ток выхода 2
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'Ток выхода 2'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValI2, row, col + 1)
#        grid.addWidget(self.checkValI2, row, col + 2)

#        #     напряжение питания
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'Напряжение питания'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValU48, row, col + 1)
#        grid.addWidget(self.checkValU48, row, col + 2)

#        #     напряжение в рабочей точке
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'Напряжение раб.т'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValUwork, row, col + 1)
#        grid.addWidget(self.checkValUwork, row, col + 2)
        
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
        
#        valI2 = 0
#        if self.checkValI2.isChecked():
#            flag, valI2 = self.checkValue(self.readValI2.text())
#            if not flag:
#                print u'Ошибка значения АЦП "Ток выхода 2"'
#                error = True
        
#        valU48 = 0
#        if self.checkValU48.isChecked():
#            flag, valU48 = self.checkValue(self.readValU48.text())
#            if not flag:
#                print u'Ошибка значения АЦП "Напряжение питания"'
#                error = True
       
#        valUwork = 0
#        if self.checkValUwork.isChecked():
#            flag, valUwork = self.checkValue(self.readValUwork.text())
#            if not flag:
#                print u'Ошибка значения АЦП "Напряжение рабочей точки"'
#                error = True
        
        # если была ошибка
        if error:
            return
        
        # добавим строку, и очистим поле ввода
        data = [valUout, valU, valI1]
        self.adjTable.addRowData(data)
        
        if self.adjTable.isFull():
            self.pAdd.setDisabled(True)
            self.pSave.setEnabled(True)
            self.pSaveAs.setEnabled(True)
                   
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
    
    def openFile(self):
        ''' (self) -> None
            
            Открытие файла прошивки с последующим заполнением таблицы.
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Открыть',
                                                    filter="HEX Files (*.hex)")
        
        try:
            fileHEX = open(filename, 'r')
            origHEX = fileHEX.read()
            fileHEX.close()
            origHEX = origHEX.splitlines()
        except:
            print u"Не удалось считать файл прошивки."
            return
        
        # поиск начала структуры данных
        posLine = 0
        posInData = -1
        for i in range(len(origHEX)):
            # -9 - служебная информация
            posInData = origHEX[i].find("9178") - 9
            if posInData >= 0:
                posLine = i
                break
        else:
            print u"Ошибка файла прошивки"
            return
        
        # 4 байта - '9178'
        # 8 байт - множитель для напряжения в рабочей точке
        # 8 байт - множитель для напряжения питания
        # 4 * (16) - массив данных int(Uацп, u, Iацп, i)
        lenght = 4 + 8 + 8 + 4 * (4 + 4 + 4 + 4)
        l = 0
        
        # извлечение нужных данных
        m = ""
        while l < lenght:
#            print "old = ", origHEX[posLine]
            data = origHEX[posLine][9 + posInData:-2]
            # пропускаем не интересующие нас 20 первых символов
            s = ""
            for char in data:
                if l >= 20:
                    s += char
                l += 1
            m += s
            posLine += 1
            posInData = 0
        
        # разбивка строки на int
        mas = []
        for i in range(16):
            tmp = m[i * 4: i * 4 + 4]
            tmp = tmp[-2:] + tmp[:2]
            mas.append(int(tmp, 16))
        # заполнение таблицы
        for row in range(4):
            self.adjTable.item(row, 0).setText(str(mas[row * 2 + 1]))
            self.adjTable.item(row, 1).setText(str(mas[row * 2 + 0]))
            self.adjTable.item(row, 2).setText(str(mas[row * 2 + 8]))
        
    def openFileHEX(self):
        ''' (self) -> str
        
            Открытие файла прошивки. Возвращает содержимое файла.
        '''
        fileHEX = open('MkUM.dat', 'r')
        text = fileHEX.read()
        fileHEX.close()

        return text
    
    def saveFileAs(self):
        ''' (self) -> None
            
            Сохранение файла с вызовом диалога "Сохранить как...".
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, u"Сохранить как...",
                                        filter="HEX Files (*.hex)")
        if filename:
            self.saveFileHEX(name=filename)
    
    def saveFileHEX(self, chacked=False, name='MkUM.hex'):
        ''' (self, name) -> None
            
            Сохраняем файл прошивки с путем/имененм name
            chacked - 
        '''
        # считаем файл прошивки и разобъем ее на строки
        try:
            origHEX = self.openFileHEX()
            origHEX = origHEX.splitlines()
        except:
            print u"Не удалось считать оригинальный файл прошивки."
            return
        
        # считаем из таблицы значения, и преобразуем их в hex-строку
        data = ""
        #    напряжение
        for row in range(4):
            tmp = self.intToHex(self.adjTable.item(row, 1).text())
            tmp += self.intToHex(self.adjTable.item(row, 0).text())
            data += tmp
        #    ток
        for row in range(4):
            tmp = self.intToHex(self.adjTable.item(row, 2).text())
            i = int(round(int(self.adjTable.item(row, 0).text()) * 1000 / 75.0))
            tmp += self.intToHex(str(i))
            data += tmp
            
        # поиск начала структуры данных
        posLine = 0
        posInData = -1
        for i in range(len(origHEX)):
            # -9 - служебная информация
            posInData = origHEX[i].find("9178") - 9
            if posInData >= 0:
                # 20 - "9178" + 2 float коэффициентов
                posInData += 20
                posLine = i
                break
        else:
            print u"Ошибка исходного файла прошивки"
            return
    
        # заполним hex-file
        # в строке данных прервые 9 байт - служебная информация
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
        while len(data) > 0:
#            print "old = ", origHEX[posLine]
            infoInLine = origHEX[posLine][:9]
            bytesInLine = int(origHEX[posLine][1:3], 16)
            # dataInLine = origHEX[posLine][9:9 + 2 * bytesInLine]
            tmp = data[:bytesInLine * 2 - posInData]
#            print "posInData = %d, bytesInLine = %d" % (posInData,bytesInLine)
#            print "tmp = %s, len = %d" % (tmp, len(tmp) / 2)
            data = data.replace(tmp, "")
            # при необходимости, добъем строку оригинальными данными
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
    
    def calcCRC(self, data):
        ''' (self, str) -> str
        
            Вычисление CRC. Возвращает сумму всех пар чисел по модулю 256 с
            последующим переводом в дополнительный формат
            
            >>>.calcCRC(':1007D00091789A998141E17A543F2B0005005800')
            'A5'
            
            >>>.calcCRC(':1007E0000A00B30014000E011E00270042004F00')
            '53'
        '''
        # при наличии признака начала строки, удалим его
        tmp = data
        if tmp[0] == ':':
            tmp = tmp[1:]
        
        # в строке должно быть четное кол-во символов
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
        
            Заполнение формы для отладки.
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
    
    # установим вид отображения
    QtGui.QApplication.setStyle('Cleanlooks')
    
    app.exec_()
