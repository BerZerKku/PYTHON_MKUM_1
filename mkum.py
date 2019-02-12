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
# ����������� ���������� ������
import resources_rc


class MyFrame(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
            �����������.
        """
        QtGui.QMainWindow.__init__(self, parent)

        # ���������� �������������� ������� ���� �
        # ��������� �� ������
        # self.setGeometry(300, 300, 250, 150)
    
        # ������� ���
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')

        # ���������� �������������� ������� ����
        # � �������� ����-��� ��������� ��������� �� ������
        # self.resize(400, 200)
        self.center()
        
        # ������������� ��� ���� � ������
        self.setWindowTitle(u'���������� ���������� ��')
        self.setWindowIcon(QtGui.QIcon(':icons/MustHave/user_24x24.png'))
        
        # ��������� ���� ����
        #   "PyQT.�������� ������� ���������� �� Python 3" ���. 53
        #   ��������� ����������� ��������
        # self.setWindowFlags(QtCore.Qt.Tool)
        #   ��������� ����������� ������
        #   "PyQT.�������� ������� ���������� �� Python 3" ���. 54
        #   MSWindowsFixedSizeDialogHint - ������ ���������  �������� ����
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # ���������� ������ ��������� � �����
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
            ��������� ���� ���������� ������.
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2
        )
    
    def show_setup_port(self):
        """
            �������� ���� ��������� �����.
        """
        # ������� ����� �� �����
        self.com_port.show()
             
    def close_port(self):
        """
            ����������� ������ � ���-������.
        """
        try:
            self.com_port.close_port()
        except Exception as e:
            QtGui.QMessageBox.warning(
                self,
                u"������",
                e.message,
                QtGui.QMessageBox.Ok
            )
        else:
            self.act_open_port.setEnabled(True)
            self.act_setup_port.setEnabled(True)
            self.act_close_port.setDisabled(True)
            self.bar_port.setText(
                u"���� {} ������.".format(self.com_port.get_port())
            )
    
    def open_port(self):
        """
            ������� ���-����. ������ ������.
        """
        try:
            self.com_port.open_port()
        except Exception as e:
            QtGui.QMessageBox.warning(
                self,
                u"������",
                e.message,
                QtGui.QMessageBox.Ok
            )
        else:
            self.act_open_port.setDisabled(True)
            self.act_setup_port.setDisabled(True)
            self.act_close_port.setEnabled(True)
            self.bar_port.setText(
                u"���� {} ������.".format(self.com_port.get_port())
            )

    def create_status_bar(self):
        """
            ������������� ������� ����������� Widget-�.
            ��������� � ������������� ������-���.
            ��������� ������ ������������� �� ����� ����.

            @return ������-��� (QtGui.QStatusBar).
        """
        self.bar = QtGui.QStatusBar()
        
        self.bar_port = QtGui.QLabel(u' %s ' % u'����')
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
        
        # ����. ����������� ������������ ����
        self.bar.setSizeGripEnabled(False)
        
        return self.bar
    
    def create_actions(self):
        """
            �������� ��������.
        """
        # ������ ���� � ������� ���������� � resources_pc.py
        # (resources.qrc)
        folder_icons = ':icons/MustHave/'
        
        # ������� �������� "�������� �����"
        # ������ ������� ������
        # � ���������� �������� � ��������
        icon = folder_icons + 'Log Out_24x24.png'
        self.act_exit = QtGui.QAction(QtGui.QIcon(icon), u'�����', self)
        self.act_exit.setShortcut("Ctrl+Q")
        self.act_exit.triggered.connect(self.close)

        # self.connect(self.aExit, QtCore.SIGNAL('triggered()'), self.close)

        # ������� �������� "��������� ����"
        icon = folder_icons + 'Previous_24x24.png'
        self.act_prev = QtGui.QAction(QtGui.QIcon(icon), u'����������', self)
        self.act_prev.triggered.connect(self.ev_prev)
        self.act_prev.setDisabled(True)
#        self.connect(self.aPrev, QtCore.SIGNAL('triggered()'),
#                     self.evPrev)
        
        # ������� �������� "��������� ����"
        icon = folder_icons + 'Next_24x24.png'
        self.act_next = QtGui.QAction(QtGui.QIcon(icon), u'���������', self)
        self.act_next.triggered.connect(self.ev_next)
        self.act_next.setDisabled(True)
#        self.connect(self.aNext, QtCore.SIGNAL('triggered()'), self.evNext)
        
        # ������� �������� "������"
        icon = folder_icons + 'help_24x24.png'
        self.act_help = QtGui.QAction(
            QtGui.QIcon(icon), u'������', self)
        self.act_help.setDisabled(True)
        
        # ������� �������� "� ���������"
        icon = folder_icons + 'information_24x24.png'
        self.act_about = QtGui.QAction(QtGui.QIcon(icon), u'� ���������', self)
        self.act_about.setDisabled(True)
        
        # �������� "������� �����
        icon = folder_icons + 'new_24x24.png'
        self.act_new_file = QtGui.QAction(QtGui.QIcon(icon), u'�����...', self)
        self.act_new_file.setShortcut("Ctrl+N")
        self.act_new_file.setDisabled(True)
        
        # ������� �������� "�������"
        icon = folder_icons + 'open_24x24.png'
        self.act_open_file = QtGui.QAction(
            QtGui.QIcon(icon), u'�������...', self)
        self.act_open_file.setShortcut("Ctrl+O")
        self.act_open_file.setDisabled(True)
        
        # ������� �������� "���������"
        icon = folder_icons + 'save_24x24.png'
        self.act_save_file = QtGui.QAction(
            QtGui.QIcon(icon), u'���������', self)
        self.act_save_file.setShortcut("Ctrl+S")
        self.act_save_file.setDisabled(True)
        
        # ������� �������� "��������� ���..."
        self.act_save_as_file = QtGui.QAction(u'��������� ���...', self)
        self.act_save_as_file.setDisabled(True)
        
        # �������� "��������� �����"
        icon = folder_icons + 'settings_24x24.png'
        self.act_setup_port = QtGui.QAction(
            QtGui.QIcon(icon), u'��������� �����', self)
        self.act_setup_port.triggered.connect(self.show_setup_port)
        self.act_setup_port.setShortcut("Alt+S")
              
        # ������� �������� "����" , ������� ����
        icon = folder_icons + 'check_24x24.png'
        self.act_open_port = QtGui.QAction(QtGui.QIcon(icon), u'����', self)

        # ������� �������� "����", ������� ����
        icon = folder_icons + 'cancel_24x24.png'
        self.act_close_port = QtGui.QAction(QtGui.QIcon(icon), u'����', self)
        self.act_close_port.setEnabled(False)
        self.act_close_port.triggered.connect(self.close_port)
        self.act_open_port.triggered.connect(self.open_port)
    
    def createToolbar(self):
        """ (self) -> None
        
            �������� ������ ������������
        """
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(self.act_exit)
        self.toolbar.addSeparator()  # �����������
        self.toolbar.addAction(self.act_prev)
        self.toolbar.addAction(self.act_next)
        self.toolbar.addSeparator()  # �����������
        self.toolbar.addAction(self.act_setup_port)
        self.toolbar.addAction(self.act_open_port)
        self.toolbar.addAction(self.act_close_port)
        self.toolbar.setAutoFillBackground(True)  # ������������ = 0
        self.addToolBar(self.toolbar)
    
    def create_menu(self):
        """ (self) -> None
        
            �������� ����
        """
        self.my_bar = self.menuBar()
        
        #     ����
        self.bar_file = self.my_bar.addMenu(u'&������')
        self.bar_file.addAction(self.act_new_file)
        self.bar_file.addAction(self.act_open_file)
        self.bar_file.addSeparator()
        self.bar_file.addAction(self.act_save_file)
        self.bar_file.addAction(self.act_save_as_file)
        self.bar_file.addSeparator()
        self.bar_file.addAction(self.act_exit)
        
        #     ���������
        self.bar_setup = self.my_bar.addMenu(u'&���������')
        self.bar_setup.addAction(self.act_setup_port)
        self.bar_setup.addAction(self.act_prev)
        self.bar_setup.addAction(self.act_next)
        
        #     ������
        self.bar_help = self.my_bar.addMenu(u'&������')
        self.bar_help.addAction(self.act_help)
        self.bar_help.addSeparator()
        self.bar_help.addAction(self.act_about)
        
        self.setStatusBar(self.create_status_bar())
    
    def create_main_window(self):
        """ (self) -> None
        
            ������������ ��������� ����
        """
        # �������� ��������� ������ � ��������� ��� � ���� ����
        self._main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self._main_widget)
        
        # ������ �������
        # self.tProject = QtGui.QTreeWidget()
        # self.tProject.setFont(QtGui.QFont('oldEnglish', 10))
        # self.tProject.setMinimumWidth(120)
        # self.tProject.setHeaderLabel(u'�����')
        # self.tProject.setHeaderHidden(True)  # ������ ���������
        # self.tProject.itemClicked.connect(self.evPressTree)
        # self.fillProjectTree(u'����')
         
        # ������� ����������
        
        # ������ � ���������
        # "PyQT.�������� ������� ���������� �� Python 3" ���. 155
        self.my_tab_widget = QtGui.QTabWidget()
        self.my_tab_widget.currentChanged.connect(self.set_command)
        self.tab_adjust_1 = tab_adjust.TabAdjust()
        self.tab_check_1 = tab_check.TabCheck()
        # self.tabAdjust2 = tab_adjust.TabAdjust()
        self.my_tab_widget.addTab(self.tab_adjust_1, u"���������� ����������")
        self.my_tab_widget.addTab(self.tab_check_1, u"�������� ����������")
        # self.myTabWidget.addTab(self.tabAdjust2, u"�������� ����������")
       
        gridTab1 = QtGui.QGridLayout()
        # gridTab1.addWidget(self.lParam, 0, 0, 3, 2)
        gridTab1.addWidget(self.my_tab_widget, 3, 0, 2, 2)
        
        # ������������ ����������
        vbox = QtGui.QVBoxLayout()
        # vbox.addWidget(self.tProject)
        # hbox = QtGui.QHBoxLayout()
        # hbox.addWidget(QtGui.QPushButton(u'��������'))
        # hbox.addWidget(QtGui.QPushButton(u'�������'))
        # vbox.addLayout(hbox)
             
        # �������������� ����������
        # hbox = QtGui.QHBoxLayout()
        # hbox.addStretch()
        # hbox.addLayout(vbox)
        vbox.addLayout(gridTab1)
        # hbox.addWidget(self.group)
        
        self._main_widget.setLayout(vbox)
        
        # ������ ��������
        # "PyQT.�������� ������� ���������� �� Python 3" ���. 152
        # self.group = QtGui.QGroupBox(u'My group')
        # self.group.setLayout(vbox)
    
    def create_port(self):
        """\
            �������� ���������� ��� ������ � ������.
        """
        self.com_port = MySerial.MySerial(parent=self)
        self.com_port.setWindowTitle(u'��������� �����')
        
        # ������� ���� ���������
        # + � ������ ������ ������ ������ ����� ������ self !!!
        self.com_port.setWindowModality(QtCore.Qt.WindowModal)
        self.connect(self.com_port,
                     QtCore.SIGNAL(
                         'readData(PyQt_PyObject, PyQt_PyObject,\
                        PyQt_PyObject)'
                     ),
                     self.protocol)
      
    def protocol(self, com, lenght, data):
        """ (self, str, int, list of str) -> None
        
            ���������� ������ �� ������� �������� ���������.
        """
        index = self.my_tab_widget.currentIndex()
        if index == 0:
            self.tab_adjust_1.readValU.setText(str(int(data[4] + data[5], 16)))
            self.tab_adjust_1.readValI1.setText(str(int(data[6] + data[7], 16)))
            # self.tabAdjust1.readValI2.setText('0')
            # self.tabAdjust1.readValU48.setText('0')
            # self.tabAdjust1.readValUwork.setText('0')
        elif index == 1:
            # �����    �������
            # 0-1, ����� � ������� ����� ���������� ������� �����
            # 2-3, ����� � ������� ����� ���������� ������� ��
            # 4-5, ����� � ������� ����� ���������� ������
            # 6-7, ����� � ������� ����� ���� ������
            u = float("%d.%d" % (int(data[4], 16), int(data[5], 16)))
            self.tab_check_1.readValU.setText('%.1f' % u)
            i = int(data[6] + data[7], 16)
            self.tab_check_1.readValI1.setText(str(i))

            try:
                r = round((1000 * u) / i, 1)
            except Exception as e:
                self.tab_check_1.readValR.setText(u'������ ����������')
            else:
                self.tab_check_1.readValR.setText(str(r))
        
        # ���������� ������ ��������� �������
        self.com_port.clrReadFlag()
    
    def set_command(self, index):
        """ (self, int) -> None
        
            ����� ������������ �������
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
