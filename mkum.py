# -*- coding: cp1251 -*-
'''
Created on 19.12.2012

@author: Shcheblykin
'''
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

import tab_adjust
import tab_check
import mySerial
# import mySpreadsheet
# подключение библиотеки иконок
import resources_rc


class MyFrame(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # определяем геометрические размеры окна и
        # положение на экране
#        self.setGeometry(300, 300, 250, 150)
    
        # внешний вид
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')

        # определяем геометрические размеры окна
        # и вызываем функ-цию установки положения на экране
#        self.resize(400, 200)
        self.center()
        
        # устанавливаем имя окна и иконку
        self.setWindowTitle(u'Калибровка измерителя УМ')
        self.setWindowIcon(QtGui.QIcon(':icons/MustHave/user_24x24.png'))
        
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
#        self.setToolTip(u'This is <b>myFrame</b> widget')
#        QtGui.QToolTip.setFont(QtGui.QFont('oldEnglish', 10))
        
        self.createPort()
        self.createMainWindow()
        self.createActions()
        self.createToolbar()
        self.createMenu()
                  
    def evPrev(self):
        pass
    
    def evNext(self):
        pass
        
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
#        self.interface.setPort(self.setupCOM.portEdit.currentText())
#        self.interface.setByteSize(self.setupCOM.byteSizeEdit.currentText())
#        self.interface.setBaudRate(self.setupCOM.baudRateEdit.currentText())
#        self.interface.setParity(self.setupCOM.parityEdit.currentText())
#        self.interface.setStopBits(self.setupCOM.stopBitsEdit.currentText())
        self.setupCOM.clearFlagModify()
    
    def evShowSetupPort(self):
        ''' (self) -> None
        
            Открытие окна настройки порта.
        '''
        # выведем форму на экран
        self.setupCOM.show()
    
    def updatePorts(self):
        self.setupCOM.fillPortBox(self.interface.getAvailablePorts(),
                                  self.interface.getPortName())
             
    def evClosePort(self):
        ''' (self) -> None
            
            Прекращение работы с ком-портом.
        '''
        try:
            self.setupCOM.closePort()
            
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
            self.setupCOM.openPort()
            
#            self.setupCOM.sendData("55 AA 01 00 01")
                
            self.aOpenPort.setDisabled(True)
            self.aSetupPort.setDisabled(True)
            self.aClosePort.setEnabled(True)
        except:
            print 'evOpenPort неудалось открыть порт'
   
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
        # задаем путь к иконкам хранящимся в resources_pc.py (resources.qrc)
        folder_icons = ':icons/MustHave/'
        
        # создаем действие "Закрытие формы"
        # задаем горячую кнопку
        # и свзязываем действие с сигналом
        icon = folder_icons + 'Log Out_24x24.png'
        self.aExit = QtGui.QAction(QtGui.QIcon(icon), u'Выход', self)
        self.aExit.setShortcut("Ctrl+Q")
        self.aExit.triggered.connect(self.close)

#        self.connect(self.aExit, QtCore.SIGNAL('triggered()'), self.close)
        
        # создаем действие "Инкремент тика"
        icon = folder_icons + 'Previous_24x24.png'
        self.aPrev = QtGui.QAction(QtGui.QIcon(icon), u'Предыдущий', self)
        self.aPrev.triggered.connect(self.evPrev)
        self.aPrev.setDisabled(True)
#        self.connect(self.aPrev, QtCore.SIGNAL('triggered()'),
#                     self.evPrev)
        
        # создаем действие "Декремент тика"
        icon = folder_icons + 'Next_24x24.png'
        self.aNext = QtGui.QAction(QtGui.QIcon(icon), u'Следующий', self)
        self.aNext.triggered.connect(self.evNext)
        self.aNext.setDisabled(True)
#        self.connect(self.aNext, QtCore.SIGNAL('triggered()'),
#                     self.evNext)
        
        # создаем действие "Помощь"
        icon = folder_icons + 'help_24x24.png'
        self.aHelp = QtGui.QAction(QtGui.QIcon(icon), u'Помощь', self)
        self.aHelp.setDisabled(True)
        
        # создаем действие "О программе"
        icon = folder_icons + 'information_24x24.png'
        self.aAbout = QtGui.QAction(QtGui.QIcon(icon), u'О программе', self)
        self.aAbout.setDisabled(True)
        
        # действие "Создать новый
        icon = folder_icons + 'new_24x24.png'
        self.aNewFile = QtGui.QAction(QtGui.QIcon(icon), u'Новый...', self)
        self.aNewFile.setShortcut("Ctrl+N")
        self.aNewFile.setDisabled(True)
        
        # создаем действие "Открыть"
        icon = folder_icons + 'open_24x24.png'
        self.aOpenFile = QtGui.QAction(QtGui.QIcon(icon), u'Открыть...', self)
        self.aOpenFile.setShortcut("Ctrl+O")
        self.aOpenFile.setDisabled(True)
        
        # создаем действие "Сохранить"
        icon = folder_icons + 'save_24x24.png'
        self.aSaveFile = QtGui.QAction(QtGui.QIcon(icon), u'Сохранить', self)
        self.aSaveFile.setShortcut("Ctrl+S")
        self.aSaveFile.setDisabled(True)
        
        # создаем действие "Сохранить как..."
        self.aSaveAsFile = QtGui.QAction(u'Сохранить как...', self)
        self.aSaveAsFile.setDisabled(True)
        
        # действие "Настройка порта"
        icon = folder_icons + 'settings_24x24.png'
        self.aSetupPort = \
            QtGui.QAction(QtGui.QIcon(icon), u'Настройки порта', self)
        self.aSetupPort.triggered.connect(self.evShowSetupPort)
        self.aSetupPort.setShortcut("Alt+S")
              
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
        self.barSetup = self.myBar.addMenu(u'&Настройка')
        self.barSetup.addAction(self.aSetupPort)
        self.barSetup.addAction(self.aPrev)
        self.barSetup.addAction(self.aNext)
        
        #     Помощь
        self.barHelp = self.myBar.addMenu(u'&Помощь')
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
#        self.tProject = QtGui.QTreeWidget()
#        self.tProject.setFont(QtGui.QFont('oldEnglish', 10))
#        self.tProject.setMinimumWidth(120)
#        self.tProject.setHeaderLabel(u'Платы')
#        self.tProject.setHeaderHidden(True)  # скрыть заголовок
#        self.tProject.itemClicked.connect(self.evPressTree)
#        self.fillProjectTree(u'МкУМ')
         
        # таблица параметров
        
        # панель с вкладками
        # "PyQT.Создание оконных приложений на Python 3" стр. 155
        self.myTabWidget = QtGui.QTabWidget()
        self.myTabWidget.currentChanged.connect(self.setCommand)
        self.tabAdjust1 = tab_adjust.TabAdjust()
        self.tabCheck1 = tab_check.TabCheck()
#        self.tabAdjust2 = tab_adjust.TabAdjust()
        self.myTabWidget.addTab(self.tabAdjust1, u"Калибровка измерителя")
        self.myTabWidget.addTab(self.tabCheck1, u"Проверка измерителя")
#        self.myTabWidget.addTab(self.tabAdjust2, u"Проверка измерителя")
       
        gridTab1 = QtGui.QGridLayout()
#        gridTab1.addWidget(self.lParam, 0, 0, 3, 2)
        gridTab1.addWidget(self.myTabWidget, 3, 0, 2, 2)
        
        # вертикальная компановка
        vbox = QtGui.QVBoxLayout()
#        vbox.addWidget(self.tProject)
#        hbox = QtGui.QHBoxLayout()
#        hbox.addWidget(QtGui.QPushButton(u'Добавить'))
#        hbox.addWidget(QtGui.QPushButton(u'Удалить'))
#        vbox.addLayout(hbox)
             
        # горизонтальная компановка
#        hbox = QtGui.QHBoxLayout()
#        hbox.addStretch()
#        hbox.addLayout(vbox)
        vbox.addLayout(gridTab1)
#        hbox.addWidget(self.group)
        
        self.mainWidget.setLayout(vbox)
        
        # группа объектов
        # "PyQT.Создание оконных приложений на Python 3" стр. 152
#        self.group = QtGui.QGroupBox(u'My group')
#        self.group.setLayout(vbox)
    
    def createPort(self):
        ''' (self) -> None
        
            Создание переменных для работы с портом.
        '''
        self.setupCOM = mySerial.mySerial(parent=self, port='COM2')
        self.setupCOM.setWindowTitle(u'Настройка порта')
        
        # сделаем окно модальным
        # + в данном случае виджет должен иметь предка self !!!
        self.setupCOM.setWindowModality(QtCore.Qt.WindowModal)
        self.connect(self.setupCOM,
                     QtCore.SIGNAL("readData(PyQt_PyObject, PyQt_PyObject,\
                     PyQt_PyObject)"),
                     self.protocol)
      
    def protocol(self, com, lenght, data):
        ''' (self, str, int, list of str) -> None
        
            Извлечение данных из посылки согласно протоколу.
        '''
        index = self.myTabWidget.currentIndex()
        if index == 0:
            self.tabAdjust1.readValU.setText(str(int(data[4] + data[5], 16)))
            self.tabAdjust1.readValI1.setText(str(int(data[6] + data[7], 16)))
#            self.tabAdjust1.readValI2.setText('0')
#            self.tabAdjust1.readValU48.setText('0')
#            self.tabAdjust1.readValUwork.setText('0')
        elif index == 1:
            # байты    функция
            # 0-1, целая и дробная части напряжения рабочей точки
            # 2-3, целая и дробная части напряжения питания УМ
            # 4-5, целая и дробная части напряжения выхода
            # 6-7, целая и дробная части тока выхода
            u = float("%d.%d" % (int(data[4], 16), int(data[5], 16)))
            self.tabCheck1.readValU.setText('%.1f' % u)
            i = int(data[6] + data[7], 16)
            self.tabCheck1.readValI1.setText(str(i))
            try:
                r = round((1000 * u) / i, 1)
            except:
                r = "Ошибка вычисления"
            self.tabCheck1.readValR.setText(str(r))
        
        # разрешение приема следующей посылки
        self.setupCOM.clrReadFlag()
    
    def setCommand(self, index):
        ''' (self, int) -> None
        
            Выбор передаваемой команды
        '''
        if index == 0:
            self.setupCOM.setCom('55 AA 02 00 02')
        elif index == 1:
            self.setupCOM.setCom('55 AA 01 00 01')
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MyFrame()
    my_frame.show()
    
    app.exec_()
