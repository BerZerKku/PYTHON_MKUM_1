# -*- coding: cp1251 -*-
'''
Created on 19.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import tab_adjust
import setupCOM
import interface


class MyFrame(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # определяем геометрические размеры окна и
        # положение на экране
#        self.setGeometry(300, 300, 250, 150)

        # определяем геометрические размеры окна
        # и вызываем функ-цию установки положения на экране
#        self.resize(400, 200)
        self.center()
        
        self.num = 0
        self.devInfo = {}
        
        # устанавливаем имя окна и иконку
        self.setWindowTitle('MkUM')
        self.setWindowIcon(QtGui.QIcon('icons/MustHave/user_24x24.png'))
        
        # установка типа окна
        #     "PyQT.Создание оконных приложений на Python 3" стр. 53
        #     установка стандартных настроек
#        self.setWindowFlags(QtCore.Qt.Tool)
        #     установка необходимых флагов
        #     "PyQT.Создание оконных приложений на Python 3" стр. 54
        #     MSWindowsFixedSizeDialogHint - запрет изменения  размеров окна
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # определяем строку подсказки и шрифт
        self.setToolTip('This is <b>myFrame</b> widget')
        QtGui.QToolTip.setFont(QtGui.QFont('oldEnglish', 10))
        
        self.createMainWindow()
        self.createActions()
        self.createToolbar()
        self.createMenu()
        self.createPort()
            
    def evPrev(self):
        pass
    
    def evNext(self):
        pass
    
    def evPressTree(self, item, a):
        ''' (self, QTreeWidgetItem, int) -> None
        
            Реакция на выбор элемента в дереве проектов.
        '''
        print 'evPressTree item = %d' % a
        print 'item =', item.text(a)
        
    def center(self):
        ''' (self) -> None
        
            Установка окна посередине экрана.
        '''
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        
    def closeEvent(self, event):
        ''' (self, PyQt4.QtGui.QCloseEvent) -> None
        
            Переопределение обработчика закрытия окна
        '''
#        reply = QtGui.QMessageBox.question(self, 'Message',
#        "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
#
#        if reply == QtGui.QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()
        pass
    
    def evCancel(self):
        if self.tProject.currentItem() in self.devInfo:
            print self.devInfo[self.tProject.currentItem()]
        else:
            pass
    
    def evSetupPort(self):
        ''' (self) -> None
            
            Установка новых значений настроек порта.
        '''
        self.interface.setPortName(self.setupCOM.portEdit.currentText())
        self.interface.setByteSize(self.setupCOM.byteSizeEdit.currentText())
        self.interface.setBaudRate(self.setupCOM.baudRateEdit.currentText())
        self.interface.setParity(self.setupCOM.parityEdit.currentText())
        self.interface.setStopBits(self.setupCOM.stopBitsEdit.currentText())
    
    def evShowSetupPort(self):
        ''' (self) -> None
        
            Открытие окна настройки порта.
        '''
        # выведем форму на экран
        self.setupCOM.show()
    
    def updatePorts(self):
        self.setupCOM.fillPortBox(self.interface.getAvailablePorts())
             
    def evClosePort(self):
        ''' (self) -> None
            
            Прекращение работы с ком-портом.
        '''
        try:
            self.interface.closePort()
            
            self.aOpenPort.setEnabled(True)
            self.aSetupPort.setEnabled(True)
            self.aClosePort.setDisabled(True)
        except:
            print 'evClosePort неудалось закрыть порт'
    
    def evOpenPort(self):
        ''' (self) -> None
        
            Открыть ком-порт. Начать работу.
        '''
        try:
            self.interface.openPort()
                
            self.aOpenPort.setDisabled(True)
            self.aSetupPort.setDisabled(True)
            self.aClosePort.setEnabled(True)
        except:
#            print 'evOpenPort неудалось открыть порт'
            pass
                  
    def fillProjectTree(self):
        ''' (self) -> None
            
            Заполнение дерева проектов.
        '''
        toplvl = QtGui.QTreeWidgetItem()
        toplvl.setText(0, '%d' % self.num)
        self.tProject.addTopLevelItem(toplvl)
        self.num += 1
        for i in range(10):
            cities = QtGui.QTreeWidgetItem()
            cities.setText(0, u'%d' % i)
            toplvl.addChild(cities)
            self.devInfo[cities] = [i, u"Текст %d" % i]
#            self.tProject.addTopLevelItem(cities)
   
    def createParamList(self):
        ''' (self) -> QTasbleWidget
            
            Создание таблицы со списком параметров
        '''
        self.lParam = QtGui.QTableWidget(3, 2)
#        self.lParam.setSizeIncrement(5, 5)
        
        cell_00 = QtGui.QTableWidgetItem(u"Версия платы:")
        cell_10 = QtGui.QTableWidgetItem(u"Частота:")
        cell_20 = QtGui.QTableWidgetItem(u"Дополнительно:")
        
        table = self.lParam
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        
        table.setItem(0, 0, cell_00)
        table.setItem(1, 0, cell_10)
        table.setItem(2, 0, cell_20)
        
        # первый столбец имеет фиксированную ширину, второй плавающую
        table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        
        # все строки кроме последней имеют фиксированную высоту
        # высота последней строки - плавающая
        for i in range(2):
            table.verticalHeader().setResizeMode(i, QtGui.QHeaderView.Fixed)
        table.verticalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
        
        # подгоним высоту строк под реальные размеры
        # и ширину первой колонки
        table.resizeRowsToContents()
        table.resizeColumnToContents(0)

        return table
        
    def updateParamList(self):
        pass
   
    def createStatusBar(self, parent=None):
        ''' (self, parent) -> QStatusBar
        
            Дополнительно создает необходимые Widget-ы.
            Создание и заполнение статус-бара.
            Последний фиджет растягивается до конца окна.
        '''
        self.bar = QtGui.QStatusBar()
        
        self.barPort = QtGui.QLabel(u' %s ' % u'Порт')
        self.barPort.setMinimumWidth(30)
        self.barPort.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.barBaudRate = QtGui.QLabel(u' %s ' % u'')
        self.barBaudRate.setMinimumWidth(30)
        self.barBaudRate.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.barSost = QtGui.QLabel(u' %s ' % u'')
        self.barSost.setMinimumWidth(20)
        
        self.bar.addWidget(self.barPort)
        self.bar.addWidget(self.barBaudRate)
        self.bar.addWidget(self.barSost, 1)
        
        # выкл. возможность растягивания окна
        self.bar.setSizeGripEnabled(False)
        
        return self.bar
    
    def createActions(self):
        ''' (self) -> None
        
            Создание действий
        '''
        # задаем путь к иконкам
        folder_icons = 'icons/MustHave/'
        
        # создаем действие "Закрытие формы"
        # задаем горячую кнопку
        # и свзязываем действие с сигналом
        icon = folder_icons + 'Log Out_24x24.png'
        self.aExit = QtGui.QAction(QtGui.QIcon(icon), u'Выход', self)
        self.aExit.setShortcut('Ctrl+Q')
        self.aExit.triggered.connect(self.close)
#        self.connect(self.aExit, QtCore.SIGNAL('triggered()'), self.close)
        
        # создаем действие "Инкремент тика"
        icon = folder_icons + 'Previous_24x24.png'
        self.aPrev = QtGui.QAction(QtGui.QIcon(icon), u'Предыдущий', self)
        self.aPrev.triggered.connect(self.evPrev)
#        self.connect(self.aPrev, QtCore.SIGNAL('triggered()'),
#                     self.evPrev)
        
        # создаем действие "Декремент тика"
        icon = folder_icons + 'Next_24x24.png'
        self.aNext = QtGui.QAction(QtGui.QIcon(icon), u'Следующий', self)
        self.aNext.triggered.connect(self.evNext)
#        self.connect(self.aNext, QtCore.SIGNAL('triggered()'),
#                     self.evNext)
        
        # создаем действие "Помощь"
        icon = folder_icons + 'help_24x24.png'
        self.aHelp = QtGui.QAction(QtGui.QIcon(icon), u'Вызов справки', self)
        
        # создаем действие "О программе"
        icon = folder_icons + 'information_24x24.png'
        self.aAbout = QtGui.QAction(QtGui.QIcon(icon), u'О программе', self)
        
        # действие "Создать новый
        icon = folder_icons + 'new_24x24.png'
        self.aNewFile = QtGui.QAction(QtGui.QIcon(icon), u'Новый...', self)
        
        # создаем действие "Открыть"
        icon = folder_icons + 'open_24x24.png'
        self.aOpenFile = QtGui.QAction(QtGui.QIcon(icon), u'Открыть...', self)
        
        # создаем действие "Сохранить"
        icon = folder_icons + 'save_24x24.png'
        self.aSaveFile = QtGui.QAction(QtGui.QIcon(icon), u'Сохранить', self)
        
        # создаем действие "Сохранить как..."
        self.aSaveAsFile = QtGui.QAction(u'Сохранить как...', self)
        
        # действие "Настройка порта"
        icon = folder_icons + 'settings_24x24.png'
        self.aSetupPort = \
            QtGui.QAction(QtGui.QIcon(icon), u'Настройки порта', self)
        self.aSetupPort.triggered.connect(self.evShowSetupPort)
              
        # создаем действие "Связь" , открыть порт
        # создаем действие "Стоп", закрыть порт
        icon = folder_icons + 'check_24x24.png'
        self.aOpenPort = QtGui.QAction(QtGui.QIcon(icon), u'Пуск', self)
        
        icon = folder_icons + 'cancel_24x24.png'
        self.aClosePort = QtGui.QAction(QtGui.QIcon(icon), u'Стоп', self)
        self.aClosePort.setEnabled(False)
        self.aClosePort.triggered.connect(self.evClosePort)
        self.aOpenPort.triggered.connect(self.evOpenPort)
    
    def createToolbar(self):
        ''' (self) -> None
        
            Создание панели инструментов
        '''
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(self.aExit)
        self.toolbar.addSeparator()  # разделитель
        self.toolbar.addAction(self.aPrev)
        self.toolbar.addAction(self.aNext)
        self.toolbar.addSeparator()  # разделитель
        self.toolbar.addAction(self.aSetupPort)
        self.toolbar.addAction(self.aOpenPort)
        self.toolbar.addAction(self.aClosePort)
        self.toolbar.setAutoFillBackground(True)  # прозрачность = 0
        self.addToolBar(self.toolbar)
    
    def createMenu(self):
        ''' (self) -> None
        
            Создание меню
        '''
        self.myBar = self.menuBar()
        
        #     Файл
        self.barFile = self.myBar.addMenu(u'&Проект')
        self.barFile.addAction(self.aNewFile)
        self.barFile.addAction(self.aOpenFile)
        self.barFile.addSeparator()
        self.barFile.addAction(self.aSaveFile)
        self.barFile.addAction(self.aSaveAsFile)
        self.barFile.addSeparator()
        self.barFile.addAction(self.aExit)
        
        #     Настройка
        self.barSetup = self.myBar.addMenu(u'Настройка')
        self.barSetup.addAction(self.aSetupPort)
        self.barSetup.addAction(self.aPrev)
        self.barSetup.addAction(self.aNext)
        
        #     Помощь
        self.barHelp = self.myBar.addMenu(u'&Справка')
        self.barHelp.addAction(self.aHelp)
        self.barHelp.addSeparator()
        self.barHelp.addAction(self.aAbout)
        
        self.setStatusBar(self.createStatusBar())
    
    def createMainWindow(self):
        ''' (self) -> None
        
            Формирование элементов окна
        '''
        # Создадим фиктивный фиджет и установим его в наше окно
        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # дерево проекта
        self.tProject = QtGui.QTreeWidget()
        self.tProject.setMinimumWidth(120)
        self.tProject.setHeaderLabel(u'Усилители')
#        self.tProject.setHeaderHidden(True)  # скрыть заголовок
        self.tProject.itemClicked.connect(self.evPressTree)
        self.fillProjectTree()
        self.fillProjectTree()
         
        # таблица параметров
        self.createParamList()
        
        # панель с вкладками
        # "PyQT.Создание оконных приложений на Python 3" стр. 155
        self.myTabWidget = QtGui.QTabWidget()
        self.tabAdjust1 = tab_adjust.TabAdjust()
        self.tabAdjust2 = tab_adjust.TabAdjust()
        self.myTabWidget.addTab(self.tabAdjust1, u"Вкладка 1")
        self.myTabWidget.addTab(self.tabAdjust2, u"Вкладка 2")
       
        gridTab1 = QtGui.QGridLayout()
        gridTab1.addWidget(self.lParam, 0, 0, 3, 2)
        gridTab1.addWidget(self.myTabWidget, 3, 0, 2, 2)
             
        # горизонтальная компановка
        hbox = QtGui.QHBoxLayout()
#        hbox.addStretch()
        hbox.addWidget(self.tProject)
        hbox.addLayout(gridTab1)
#        hbox.addWidget(self.group)
        
        self.mainWidget.setLayout(hbox)
        
        # группа объектов
        # "PyQT.Создание оконных приложений на Python 3" стр. 152
#        self.group = QtGui.QGroupBox(u'My group')
#        self.group.setLayout(vbox)
    
    def createPort(self):
        self.interface = interface.Interface()
        
        # создадим виджет настройки порта
        self.setupCOM = setupCOM.SetupCOM(parent=self)
        self.setupCOM.setWindowTitle(self.aSetupPort.text())
        self.setupCOM.setWindowIcon(self.aSetupPort.icon())
        # заполним поля на форме
        self.updatePorts()
        self.setupCOM.fillBaudRateBox(self.interface.getAvailableBaudRates())
        self.setupCOM.fillStopBitsBox(self.interface.getAvailableStopBits())
        self.setupCOM.fillByteSize(self.interface.getAvailableByteSize())
        self.setupCOM.fillParityBox(self.interface.getAvailableParities())
        
        # настройка сигналов и слотов
        #    сканирование доступных портов
        self.setupCOM.pScan.clicked.connect(self.updatePorts)
        #    "Отменить" - просто закрываем форму
        self.setupCOM.pAbort.clicked.connect(self.setupCOM.close)
        #    "Принять" - устанавливаем новые настройки и зкрываем форму
        self.setupCOM.pApply.clicked.connect(self.evSetupPort)
        self.setupCOM.pApply.clicked.connect(self.setupCOM.close)
                
        # сделаем окно модальным
        # + в данном случае виджет должен иметь предка self !!!
        self.setupCOM.setWindowModality(QtCore.Qt.WindowModal)
                    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    my_frame = MyFrame()
    my_frame.show()
    app.exec_()
