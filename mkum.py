# -*- coding: cp1251 -*-
"""
Created on 19.12.2012

@author: Shcheblykin
"""
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
# from PyQt4.QtCore import Qt

import tab_adjust
import tab_check
import MySerial
# import mySpreadsheet
# подключение библиотеки иконок
import resources_rc


class MyFrame(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
            Конструктор.
        """
        QtGui.QMainWindow.__init__(self, parent)

        # определяем геометрические размеры окна и
        # положение на экране
        # self.setGeometry(300, 300, 250, 150)
    
        # внешний вид
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')

        # определяем геометрические размеры окна
        # и вызываем функ-цию установки положения на экране
        # self.resize(400, 200)
        self.center()
        
        # устанавливаем имя окна и иконку
        self.setWindowTitle(u'Калибровка измерителя УМ')
        self.setWindowIcon(QtGui.QIcon(':icons/MustHave/user_24x24.png'))
        
        # установка типа окна
        #   "PyQT.Создание оконных приложений на Python 3" стр. 53
        #   установка стандартных настроек
        # self.setWindowFlags(QtCore.Qt.Tool)
        #   установка необходимых флагов
        #   "PyQT.Создание оконных приложений на Python 3" стр. 54
        #   MSWindowsFixedSizeDialogHint - запрет изменения  размеров окна
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # определяем строку подсказки и шрифт
        # self.setToolTip(u'This is <b>myFrame</b> widget')
        # QtGui.QToolTip.setFont(QtGui.QFont('oldEnglish', 10))
        
        self.create_port()
        self.create_main_window()
        self.create_actions()
        self.createToolbar()
        self.create_menu()
                  
    def ev_prev(self):
        """
            None
        """
        pass
    
    def ev_next(self):
        """
            None
        """
        pass
        
    def center(self):
        """
            Установка окна посередине экрана.
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2
        )
    
    def show_setup_port(self):
        """
            Открытие окна настройки порта.
        """
        # выведем форму на экран
        self.com_port.show()
             
    def close_port(self):
        """
            Прекращение работы с ком-портом.
        """
        try:
            self.com_port.close_port()
        except Exception as e:
            QtGui.QMessageBox.warning(
                self,
                u"Ошибка",
                e.message,
                QtGui.QMessageBox.Ok
            )
        else:
            self.act_open_port.setEnabled(True)
            self.act_setup_port.setEnabled(True)
            self.act_close_port.setDisabled(True)
            self.bar_port.setText(
                u"Порт {} закрыт.".format(self.com_port.get_port())
            )
    
    def open_port(self):
        """
            Открыть ком-порт. Начать работу.
        """
        try:
            self.com_port.open_port()
        except Exception as e:
            QtGui.QMessageBox.warning(
                self,
                u"Ошибка",
                e.message,
                QtGui.QMessageBox.Ok
            )
        else:
            self.act_open_port.setDisabled(True)
            self.act_setup_port.setDisabled(True)
            self.act_close_port.setEnabled(True)
            self.bar_port.setText(
                u"Порт {} открыт.".format(self.com_port.get_port())
            )

    def create_status_bar(self):
        """
            Дополнительно создает необходимые Widget-ы.
            Создается и заполненяется статус-бар.
            Последний виджет растягивается до конца окна.

            @return Статус-бар (QtGui.QStatusBar).
        """
        self.bar = QtGui.QStatusBar()
        
        self.bar_port = QtGui.QLabel(u' %s ' % u'Порт')
        self.bar_port.setMinimumWidth(30)
        self.bar_port.setAlignment(QtCore.Qt.AlignHCenter)
        
        # self.barBaudRate = QtGui.QLabel(u' %s ' % u'')
        # self.barBaudRate.setMinimumWidth(30)
        # self.barBaudRate.setAlignment(QtCore.Qt.AlignHCenter)
        #
        # self.barSost = QtGui.QLabel(u' %s ' % u'')
        # self.barSost.setMinimumWidth(20)
        
        self.bar.addWidget(self.bar_port)
        # self.bar.addWidget(self.barBaudRate)
        # self.bar.addWidget(self.barSost, 1)
        
        # выкл. возможность растягивания окна
        self.bar.setSizeGripEnabled(False)
        
        return self.bar
    
    def create_actions(self):
        """
            Создание действий.
        """
        # задаем путь к иконкам хранящимся в resources_pc.py
        # (resources.qrc)
        folder_icons = ':icons/MustHave/'
        
        # создаем действие "Закрытие формы"
        # задаем горячую кнопку
        # и свзязываем действие с сигналом
        icon = folder_icons + 'Log Out_24x24.png'
        self.act_exit = QtGui.QAction(QtGui.QIcon(icon), u'Выход', self)
        self.act_exit.setShortcut("Ctrl+Q")
        self.act_exit.triggered.connect(self.close)

        # self.connect(self.aExit, QtCore.SIGNAL('triggered()'), self.close)

        # создаем действие "Инкремент тика"
        icon = folder_icons + 'Previous_24x24.png'
        self.act_prev = QtGui.QAction(QtGui.QIcon(icon), u'Предыдущий', self)
        self.act_prev.triggered.connect(self.ev_prev)
        self.act_prev.setDisabled(True)
#        self.connect(self.aPrev, QtCore.SIGNAL('triggered()'),
#                     self.evPrev)
        
        # создаем действие "Декремент тика"
        icon = folder_icons + 'Next_24x24.png'
        self.act_next = QtGui.QAction(QtGui.QIcon(icon), u'Следующий', self)
        self.act_next.triggered.connect(self.ev_next)
        self.act_next.setDisabled(True)
#        self.connect(self.aNext, QtCore.SIGNAL('triggered()'), self.evNext)
        
        # создаем действие "Помощь"
        icon = folder_icons + 'help_24x24.png'
        self.act_help = QtGui.QAction(
            QtGui.QIcon(icon), u'Помощь', self)
        self.act_help.setDisabled(True)
        
        # создаем действие "О программе"
        icon = folder_icons + 'information_24x24.png'
        self.act_about = QtGui.QAction(QtGui.QIcon(icon), u'О программе', self)
        self.act_about.setDisabled(True)
        
        # действие "Создать новый
        icon = folder_icons + 'new_24x24.png'
        self.act_new_file = QtGui.QAction(QtGui.QIcon(icon), u'Новый...', self)
        self.act_new_file.setShortcut("Ctrl+N")
        self.act_new_file.setDisabled(True)
        
        # создаем действие "Открыть"
        icon = folder_icons + 'open_24x24.png'
        self.act_open_file = QtGui.QAction(
            QtGui.QIcon(icon), u'Открыть...', self)
        self.act_open_file.setShortcut("Ctrl+O")
        self.act_open_file.setDisabled(True)
        
        # создаем действие "Сохранить"
        icon = folder_icons + 'save_24x24.png'
        self.act_save_file = QtGui.QAction(
            QtGui.QIcon(icon), u'Сохранить', self)
        self.act_save_file.setShortcut("Ctrl+S")
        self.act_save_file.setDisabled(True)
        
        # создаем действие "Сохранить как..."
        self.act_save_as_file = QtGui.QAction(u'Сохранить как...', self)
        self.act_save_as_file.setDisabled(True)
        
        # действие "Настройка порта"
        icon = folder_icons + 'settings_24x24.png'
        self.act_setup_port = QtGui.QAction(
            QtGui.QIcon(icon), u'Настройки порта', self)
        self.act_setup_port.triggered.connect(self.show_setup_port)
        self.act_setup_port.setShortcut("Alt+S")
              
        # создаем действие "Пуск" , открыть порт
        icon = folder_icons + 'check_24x24.png'
        self.act_open_port = QtGui.QAction(QtGui.QIcon(icon), u'Пуск', self)

        # создаем действие "Стоп", закрыть порт
        icon = folder_icons + 'cancel_24x24.png'
        self.act_close_port = QtGui.QAction(QtGui.QIcon(icon), u'Стоп', self)
        self.act_close_port.setEnabled(False)
        self.act_close_port.triggered.connect(self.close_port)
        self.act_open_port.triggered.connect(self.open_port)
    
    def createToolbar(self):
        """ (self) -> None
        
            Создание панели инструментов
        """
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(self.act_exit)
        self.toolbar.addSeparator()  # разделитель
        self.toolbar.addAction(self.act_prev)
        self.toolbar.addAction(self.act_next)
        self.toolbar.addSeparator()  # разделитель
        self.toolbar.addAction(self.act_setup_port)
        self.toolbar.addAction(self.act_open_port)
        self.toolbar.addAction(self.act_close_port)
        self.toolbar.setAutoFillBackground(True)  # прозрачность = 0
        self.addToolBar(self.toolbar)
    
    def create_menu(self):
        """ (self) -> None
        
            Создание меню
        """
        self.my_bar = self.menuBar()
        
        #     Файл
        self.bar_file = self.my_bar.addMenu(u'&Проект')
        self.bar_file.addAction(self.act_new_file)
        self.bar_file.addAction(self.act_open_file)
        self.bar_file.addSeparator()
        self.bar_file.addAction(self.act_save_file)
        self.bar_file.addAction(self.act_save_as_file)
        self.bar_file.addSeparator()
        self.bar_file.addAction(self.act_exit)
        
        #     Настройка
        self.bar_setup = self.my_bar.addMenu(u'&Настройка')
        self.bar_setup.addAction(self.act_setup_port)
        self.bar_setup.addAction(self.act_prev)
        self.bar_setup.addAction(self.act_next)
        
        #     Помощь
        self.bar_help = self.my_bar.addMenu(u'&Помощь')
        self.bar_help.addAction(self.act_help)
        self.bar_help.addSeparator()
        self.bar_help.addAction(self.act_about)
        
        self.setStatusBar(self.create_status_bar())
    
    def create_main_window(self):
        """ (self) -> None
        
            Формирование элементов окна
        """
        # Создадим фиктивный фиджет и установим его в наше окно
        self._main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self._main_widget)
        
        # дерево проекта
        # self.tProject = QtGui.QTreeWidget()
        # self.tProject.setFont(QtGui.QFont('oldEnglish', 10))
        # self.tProject.setMinimumWidth(120)
        # self.tProject.setHeaderLabel(u'Платы')
        # self.tProject.setHeaderHidden(True)  # скрыть заголовок
        # self.tProject.itemClicked.connect(self.evPressTree)
        # self.fillProjectTree(u'МкУМ')
         
        # таблица параметров
        
        # панель с вкладками
        # "PyQT.Создание оконных приложений на Python 3" стр. 155
        self.my_tab_widget = QtGui.QTabWidget()
        self.my_tab_widget.currentChanged.connect(self.set_command)
        self.tab_adjust_1 = tab_adjust.TabAdjust()
        self.tab_check_1 = tab_check.TabCheck()
        # self.tabAdjust2 = tab_adjust.TabAdjust()
        self.my_tab_widget.addTab(self.tab_adjust_1, u"Калибровка измерителя")
        self.my_tab_widget.addTab(self.tab_check_1, u"Проверка измерителя")
        # self.myTabWidget.addTab(self.tabAdjust2, u"Проверка измерителя")
       
        gridTab1 = QtGui.QGridLayout()
        # gridTab1.addWidget(self.lParam, 0, 0, 3, 2)
        gridTab1.addWidget(self.my_tab_widget, 3, 0, 2, 2)
        
        # вертикальная компановка
        vbox = QtGui.QVBoxLayout()
        # vbox.addWidget(self.tProject)
        # hbox = QtGui.QHBoxLayout()
        # hbox.addWidget(QtGui.QPushButton(u'Добавить'))
        # hbox.addWidget(QtGui.QPushButton(u'Удалить'))
        # vbox.addLayout(hbox)
             
        # горизонтальная компановка
        # hbox = QtGui.QHBoxLayout()
        # hbox.addStretch()
        # hbox.addLayout(vbox)
        vbox.addLayout(gridTab1)
        # hbox.addWidget(self.group)
        
        self._main_widget.setLayout(vbox)
        
        # группа объектов
        # "PyQT.Создание оконных приложений на Python 3" стр. 152
        # self.group = QtGui.QGroupBox(u'My group')
        # self.group.setLayout(vbox)
    
    def create_port(self):
        """\
            Создание переменных для работы с портом.
        """
        self.com_port = MySerial.MySerial(parent=self)
        self.com_port.setWindowTitle(u'Настройка порта')
        
        # сделаем окно модальным
        # + в данном случае виджет должен иметь предка self !!!
        self.com_port.setWindowModality(QtCore.Qt.WindowModal)
        self.connect(self.com_port,
                     QtCore.SIGNAL(
                         'readData(PyQt_PyObject, PyQt_PyObject,\
                        PyQt_PyObject)'
                     ),
                     self.protocol)
      
    def protocol(self, com, lenght, data):
        """ (self, str, int, list of str) -> None
        
            Извлечение данных из посылки согласно протоколу.
        """
        index = self.my_tab_widget.currentIndex()
        if index == 0:
            self.tab_adjust_1.readValU.setText(str(int(data[4] + data[5], 16)))
            self.tab_adjust_1.readValI1.setText(str(int(data[6] + data[7], 16)))
            # self.tabAdjust1.readValI2.setText('0')
            # self.tabAdjust1.readValU48.setText('0')
            # self.tabAdjust1.readValUwork.setText('0')
        elif index == 1:
            # байты    функция
            # 0-1, целая и дробная части напряжения рабочей точки
            # 2-3, целая и дробная части напряжения питания УМ
            # 4-5, целая и дробная части напряжения выхода
            # 6-7, целая и дробная части тока выхода
            u = float("%d.%d" % (int(data[4], 16), int(data[5], 16)))
            self.tab_check_1.readValU.setText('%.1f' % u)
            i = int(data[6] + data[7], 16)
            self.tab_check_1.readValI1.setText(str(i))

            try:
                r = round((1000 * u) / i, 1)
            except Exception as e:
                self.tab_check_1.readValR.setText(u'Ошибка вычисления')
            else:
                self.tab_check_1.readValR.setText(str(r))
        
        # разрешение приема следующей посылки
        self.com_port.clrReadFlag()
    
    def set_command(self, index):
        """ (self, int) -> None
        
            Выбор передаваемой команды
        """
        if index == 0:
            self.com_port.set_com('55 AA 02 00 02')
        elif index == 1:
            self.com_port.set_com('55 AA 01 00 01')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    my_frame = MyFrame()
    my_frame.show()
    
    app.exec_()
