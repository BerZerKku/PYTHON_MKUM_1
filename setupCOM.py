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
    
        Widget работы с ком-портом.
        Имеется возможность поиска доступных портов в системе,
        настройка параметров работы, открытие и закрытие порта.
        Полученная/отправленная инф-ия выводится на экран.
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        # установка фиксированного размера окна
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # флаг наличия изменений
        self._modify = False
        
        # создание элементов виджета
        self.createWidget()

    def fillPortBox(self, data, val='COM1'):
        ''' (self, list, str) -> None
        
            Заполнение раскрывающегося списка портов данными data
            ри наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка скоростей данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка стоп-битов данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка четностей данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
        
            Заполнение раскрывающегося списка кол-ва бит данных данными data.
            При наличии в списке значения val, оно будет выбрано.
        '''
        # Заполним состояние флага модификации и не будет сбрасывать,
        # если он был установлен
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
            
            Установка флага наличия изменений параметров.
            val - индекс установленного элемента
        '''
        self._modify = True
        self.pApply.setEnabled(True)
    
    def isFlagModify(self):
        ''' (self) -> None
        
            Проверка наличия изменений параметров.
        '''
        return self._modify
        
    def clearFlagModify(self):
        ''' (self) -> None
            
            Сброс флага наличия изменений параметров
        '''
        self._modify = False
        self.pApply.setDisabled(True)
    
    def debug(self):
        ''' (self, list) -> None
        
            Отладка
        '''
        self.portEdit.addItem('COM121')

    def createWidget(self):
        ''' (self, bool) -> None
        
            Формирование элементов окна.
            debug - отвечает за выбор режима:
                False - рабочий (по умолчанию)
                True - отладка
        '''
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.portEdit = QtGui.QComboBox()
        self.portLabel = QtGui.QLabel(u'Имя:')
        vboxl.addWidget(self.portLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.portEdit)
        
        self.baudRateEdit = QtGui.QComboBox()
        self.baudRateLabel = QtGui.QLabel(u'Скорость бит/с:')
        vboxl.addWidget(self.baudRateLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.baudRateEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        groupbox1 = QtGui.QGroupBox(u'Основные')
        groupbox1.setLayout(hbox)
        
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self.byteSizeEdit = QtGui.QComboBox()
        self.byteSizeLabel = QtGui.QLabel(u'Биты данных:')
        vboxl.addWidget(self.byteSizeLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.byteSizeEdit)
        
        self.parityEdit = QtGui.QComboBox()
        self.parityLabel = QtGui.QLabel(u'Четность:')
        vboxl.addWidget(self.parityLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.parityEdit)
        
        self.stopBitsEdit = QtGui.QComboBox()
        self.stopBitsLabel = QtGui.QLabel(u'Стоповые биты:')
        vboxl.addWidget(self.stopBitsLabel, alignment=QtCore.Qt.AlignRight)
        vboxe.addWidget(self.stopBitsEdit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        
        groupbox2 = QtGui.QGroupBox(u'Формат данных')
        groupbox2.setLayout(hbox)
        
        self.pScan = QtGui.QPushButton(u'Обновить')
        self.connect(self.pScan, QtCore.SIGNAL('clicked()'), self.debug)
        
        self.pApply = QtGui.QPushButton(u'Принять')
        self.pAbort = QtGui.QPushButton(u'Отменить')
        
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
        
        # подключим сигналы
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
