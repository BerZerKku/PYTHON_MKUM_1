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
        self.adjTable.horizontalHeaderItem(0).setText(u"Uвых,В")
        self.adjTable.horizontalHeaderItem(1).setText(u"Uизм,В")
        self.adjTable.horizontalHeaderItem(2).setText(u"Iвых,мА")
        self.adjTable.horizontalHeaderItem(3).setText(u"Iизм,мА")
        self.adjTable.horizontalHeaderItem(4).setText(u"Rизм,Ом")
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
#        self.entValU = QtGui.QLineEdit(u'Uвых')
#        self.entValU.setValidator(QtGui.QDoubleValidator(1, 99, 1, self))
#        self.entValU.clear()  # очистка текста
        self.entValU = QtGui.QDoubleSpinBox()
        self.entValU.setRange(0.0, 100.0)
        self.entValU.setDecimals(1)
        #    уберем контекстное меню, т.к. могут быть проблемы с 'Undo'
        self.entValU.setContextMenuPolicy(Qt.NoContextMenu)
#        self.entValU.textChanged.connect(self.valUChange)
        self.entValU.valueChanged.connect(self.valUChange)
          
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
        
        self.readValR = QtGui.QLineEdit(u'Нет данных')
        self.readValR.setDisabled(True)
#        self.readValI2.setContextMenuPolicy(Qt.NoContextMenu)
        self.checkValR = QtGui.QCheckBox()
        self.checkValR.setChecked(True)
        self.checkValR.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
#        self.readValU48 = QtGui.QLineEdit(u'Нет данных')
#        self.readValU48.setDisabled(True)
# #        self.readValU48.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValU48 = QtGui.QCheckBox()
#        self.checkValU48.setChecked(False)
#        self.checkValU48.setDisabled(True)
#        self.checkValU48.setToolTip(u"Вкл./выкл. калибровки параметра.")

#        self.readValUwork = QtGui.QLineEdit(u'Нет данных')
#        self.readValUwork.setDisabled(True)
# #        self.readValUwork.setContextMenuPolicy(Qt.NoContextMenu)
#        self.checkValUwork = QtGui.QCheckBox()
#        self.checkValUwork.setChecked(False)
#        self.checkValUwork.setDisabled(True)
#        self.checkValUwork.setToolTip(u"Вкл./выкл. калибровки параметра.")
        
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.saveFile)
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
        grid.addLayout(hbox1, 7, 0, 1, 2)
        
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
        grid.addWidget(QtGui.QLabel(u'Напряжение выхода, В'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValU, row, col + 1)
        grid.addWidget(self.checkValU, row, col + 2)
        
        #     ток выхода 1
        row += 1
        grid.addWidget(QtGui.QLabel(u'Ток выхода, мА'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValI1, row, col + 1)
        grid.addWidget(self.checkValI1, row, col + 2)
        
        #     сопротивление
        row += 1
        grid.addWidget(QtGui.QLabel(u'Сопротивление, Ом'), row, col,
                       alignment=Qt.AlignRight)
        grid.addWidget(self.readValR, row, col + 1)
        grid.addWidget(self.checkValR, row, col + 2)
        
        #     напряжение питания
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'Напряжение питания, В'), row, col,
#                       alignment=Qt.AlignRight)
#        grid.addWidget(self.readValU48, row, col + 1)
#        grid.addWidget(self.checkValU48, row, col + 2)
       
#        #     напряжение в рабочей точке
#        row += 1
#        grid.addWidget(QtGui.QLabel(u'Напряжение раб.тб В'), row, col,
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
        flag, valUout = self.checkValue(self.entValU.text(), 1, 99)
#        self.entValU.setText("")
        if not flag:
            print u"Ошибка введенного значения напряжения выхода"
            error = True
            
        valU = 0
        if self.checkValU.isChecked():
            flag, valU = self.checkValue(self.readValU.text(), 1, 99)
            if not flag:
                print u'Ошибка значения АЦП "Напряжени выхода"'
                error = True
        
        valI1 = 0
        if self.checkValI1.isChecked():
            flag, valI1 = self.checkValue(self.readValI1.text(), 1, 1500)
            if not flag:
                print u'Ошибка значения АЦП "Ток выхода 1"'
                error = True
            else:
                valI1 = int(valI1)
        
        valI1ent = int(round((valUout * 1000) / 75.0))
        
        valR = 0
        if self.checkValR.isChecked():
            flag, valR = self.checkValue(self.readValR.text(), 1, 999)
            if not flag:
                print u'Ошибка значения АЦП "Сопротивление"'
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
            QtGui.QMessageBox.warning(self, u'Ошибка ввода',
                                      u'Некорректные данные АЦП.')
            return
        
        # добавим строку, и очистим поле ввода
        data = [valUout, valU, valI1ent, valI1, valR]
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
            
    def checkValue(self, val, minVal, maxVal):
        ''' (self, str, number, number) -> bool, float
        
            Входная строка преобразуется в число val. Если полученное значение
            выходит за диапазон min <= val <= max, возвращается False, val.
            Иначе True, val.
            
            >>> .checkValue("123.7", 1, 99)
            (False, 0)
            >>> .checkValue("123.7", 1, 199)
            (True, 123.7)
        '''
        
        sost = False
        
        try:
            # при наличии разделительной запятой в тексте, заменим на точку
            val = val.replace(',', '.')
            val = float(val)
            sost = True
        except:
            print u"Error:",
            print u'Ошибка преобразования строки в float', self
            val = 0

        if sost:
            if not (val >= minVal and val <= maxVal):
                val = 0
                sost = False
        
        return sost, val
    
    def openFile(self):
        ''' (self) -> None
            
            Открытие файла данных с последующим заполнением таблицы.
        '''
        filename = QtGui.QFileDialog.getOpenFileName(self, u"Открыть",
                                        filter="Data Files (*.dat)")
        
        if not filename:
            return
        
        # считывание сожержимого файла
        f = open(filename, 'rb')
        data_bin = f.read()
        f.close()
        
        data = []
        for char in data_bin:
            data.append(char.encode('hex').upper())
        del data_bin
        
        # сопротивление
        r = my_func.strHexToInt(data[0])
        print r
        
        # напряжения измеренные прибором
        uOut = []
        for i in range(6):
            u = my_func.strHexToInt(data[i + 1])
            if u == 0:
                break
            uOut.append(u)
        print uOut
        
        # ток измеренный прибором
        if r == 0:
            print u'Error:'
            print u'Считанное сопротивление из файла равно 0'
            raise ValueError
        iOut = []
        for u in uOut:
            iOut.append(int(round(u * 1000 / r)))
        print iOut
        
        # ток 
        
         
    def saveFileAs(self):
        ''' (self) -> None
            
            Сохранение файла с вызовом диалога "Сохранить как...".
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, u"Сохранить как...",
                                        filter="Data Files (*.dat)")
        if filename:
            self.saveFile(name=filename)
    
    def saveFile(self, chacked=False, name='MkUM.dat'):
        ''' (self, name) -> None
            
            Сохранение файла данных с путем/имененм name
            chacked - для SIGNAL от кнопки
        '''
        # считаем файл прошивки и разобъем ее на строки
        pass
  
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
        
#    def debugSaveFile(self, data):
#        ''' (self) -> None
      
#            Заполнение формы для отладки.
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
    # my_frame.debugSaveFile([[43, 5, 88, 10, 179, 20, 270, 30],
    #                        [39, 66, 79, 133, 159, 266, 242, 400]])
#    my_frame.debugSaveFile([[40, 5, 81, 10, 172, 20, 263, 30],
#                            [45, 66, 90, 133, 187, 266, 283, 400]])
    
    # установим вид отображения
    QtGui.QApplication.setStyle('Cleanlooks')
    
    app.exec_()


# import unittest
#
#
# class TestTabCheck(unittest.TestCase):
#    """${short_summary_of_testcase}
#    """
#    def setUp(self):
# #        self.testFrame = TabCheck()
#        self.app = QtGui.QApplication(sys.argv)
#        self.form = TabCheck()

#    def tearDown(self):
#        """${no_tearDown_required}
#        """
#    pass  # skip tearDown
#
#    def testIntToHex(self):
#        """${short_description_of_test}
#        """
# #        print self.testFrame
#        self.assertEqual(self.form.intToHex(5), '0500')
#        self.assertEqual(self.form.intToHex(270), '0E01')

#    def testCalcCRC(self):
#        self.assertEqual(
#                self.form.calcCRC(':1007D00091789A998141E17A543F2B0005005800')
#                ,'A5')
#        self.assertEqual(
#                self.form.calcCRC(':1007E0000A00B30014000E011E00270042004F00')
#                ,'53')
