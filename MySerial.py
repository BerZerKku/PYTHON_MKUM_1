# -*- coding: cp1251 -*-
"""
Created on 24.12.2012

@author: Shcheblykin

python: 2.7.15
pySerial: 3.4
pyQT: 4.9.5-1 x64

"""
import sys
import serial
from PyQt4 import QtGui
from PyQt4 import QtCore
import time


class MySerial(QtGui.QWidget):
    """
        Widget ������ � ���-������.
        ������� ����������� ������ ��������� ������ � �������,
        ��������� ���������� ������, �������� � �������� �����.
    """

    PARITY = {
        'N': 'None', 
        'O': 'Odd', 
        'E': 'Even', 
        'M': 'Mark', 
        'S': 'Space'
    }

    def __init__(self, parent=None):
        """
            �����������.
        """
        QtGui.QWidget.__init__(self, parent)

        # ��������� �������������� ������� ����
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)

        # ���������������� ����
        self._port = serial.Serial()
        self._port.timeout = 0;

        # ��������� ����������������� �����
        self._set_port();
        self._set_baudrate()
        self._set_bytesize()
        self._set_parity()
        self._set_stopbits()

        # �������� ��������� �������
        self._create_widget()

        self.set_com("55 AA 02 00 02")
        
        # ���� �������� ������� (True - ���� �������)
        self._bRead = False
        # ����� �������� ��������� ����� �������� ���������
        self._cnt = 0
        # ������ ������
        self._data = []
        # ���-�� ���� ������
        self._length = 0
        # ����������� �����
        self._crc = 0
        
        # ������ �����������
        self._timerTr = QtCore.QTimer()
        self._timerTr.setInterval(500)
        self._timerTr.timeout.connect(self._cycle_send)
        
        # ������ ���������
        self._timerRc = QtCore.QTimer()
        self._timerRc.setInterval(5)
        self._timerRc.timeout.connect(self._cycle_receive)
        
        # ����
        self._clock = QtCore.QTime.currentTime()

    def show(self):
        """
            ��������������� ������ ����������� ����.
            ����������� ������ ��������� ������.
            ������������ ������� ��������� �����.
        """
        self._refresh_ports()

        i = self._edit_port.findText(self._port.port)
        self._edit_port.setCurrentIndex(0 if i < 0 else i)

        i = self._edit_baudrate.findText(str(self._port.baudrate))
        self._edit_baudrate.setCurrentIndex(0 if i < 0 else i)

        i = self._edit_stopbits.findText(str(self._port.stopbits))
        self._edit_stopbits.setCurrentIndex(0 if i < 0 else i)

        i = self._edit_parity.findText(str(self._port.parity))
        self._edit_parity.setCurrentIndex(0 if i < 0 else i)

        i = self._edit_bytesize.findText(str(self._port.bytesize))
        self._edit_bytesize.setCurrentIndex(0 if i < 0 else i)

        super(MySerial, self).show()

    def open_port(self):
        """
            ������ ������ � ������. � ������ ������ ���������� False.
        """
        try:
            self._port.open()
        except serial.SerialException:
            raise Exception(
                u'������ �������� �����. \n\n {!r}'.format(self._port)
            )
        except Exception:
            raise
        else:
            self._timerTr.start()
            self._timerRc.start()
            
    def close_port(self):
        """
            ��������� ������ � ������. � ������ ������ ���������� False.
        """
        try:
            self._port.close()
        except serial.SerialException:
            raise Exception(
                u'������ �������� �����. \n\n {!r}'.format(self._port)
            )
        except Exception:
            raise
        else:
            self._timerTr.stop()
            self._timerRc.stop()
    
    def is_open(self):
        """
            @return True ���� ���� ������, ����� false.
        """
        return self._port.is_open
        
    def _refresh_ports(self):
        """
            ���������� ���������� � ����� ��������.
        """
        # ���������� ������� ����
        port = self._edit_port.currentText();

        # ��������� ������ ��������� ������
        self._edit_port.clear()
        self._edit_port.addItems([str(x) for x in self._scan_ports()])

        # ��������� � ������ ������� "��������" �����
        i = self._edit_port.findText(str(self._port.port))
        if i >= 0:
            # ���� �� ����, ������������� ���
            self._edit_port.setCurrentIndex(i)
        else:
            # ���� ���, �� ��������� ������� ���������� ��������� �����
            i = self._edit_port.findText(port)
            if i >= 0:
                # ���� �� ����, �� ������������� ���
                self._edit_port.setCurrentIndex(i)
            else:
                # ���� ���, �� ������������ ������ � ������
                self._edit_port.setCurrentIndex(0)
        
    def _set_port(self, val=None):
        """
            ��������� �����.
        """
        if val is None:
            val = self._scan_ports()[0]

        try:
            self._port.setPort(str(val))
        except Exception:
            raise Exception(
                u'������ ������ �����: {!r}.'.format(val)
            )

    def get_port(self):
        """
            @return �������� �������� Com-����� (unicode).
        """
        return self._port.port

    def _set_baudrate(self, val=1200):
        """
            ��������� �������� ������ ����� val, ���/�.
        """
        try:
            self._port.baudrate = int(val);
        except ValueError:
            raise Exception(
                u'������ ��������� �������� �����: {!r}.'.format(val)
            )

    def _set_bytesize(self, val=serial.EIGHTBITS):
        """\
            ��������� ���-�� ��� ������ val.
        """
        try:
            self._port.bytesize = int(val);
        except ValueError:
            raise Exception(
                u'������ ��������� ���������� ���� �����: {!r}.'.format(val)
            )
        
    def _set_parity(self, val=serial.PARITY_NONE):
        """\
            ��������� �������� val.
        """
        try:
            self._port.parity = str(val)[0]
        except ValueError:
            raise Exception(
                u'������ ��������� �������� �������� �����: {!r}.'.format(val)
            )

    def _set_stopbits(self, val=serial.STOPBITS_TWO):
        """\
            ��������� ���-�� ����-��� val.
        """


        try:
            val = float(val)
            val = int(val) if int(val) == val else val
            self._port.stopbits = val
        except ValueError:
            raise Exception(
                u'������ ��������� ���-�� ���� ��� �����: {!r}.'.format(val)
            )
    
    def _set_settings(self, checked=False):
        """
            ��������� ����� �������� �����.

            �������� checked, ������������ ��� SIGNAL ������� ������
        """
        self._set_port(self._edit_port.currentText())
        self._set_baudrate(self._edit_baudrate.currentText())
        self._set_bytesize(self._edit_bytesize.currentText())
        self._set_parity(self._edit_parity.currentText())
        self._set_stopbits(self._edit_stopbits.currentText())
        self.close()

    def _scan_ports(self):
        """
            ������ ������.

            return ���������� ������ ��������� ������.
        """

        available = []
        for i in range(256):
            try:
                s = serial.Serial('COM' + str(i))
            except serial.SerialException:
                pass
            except Exception:
                raise Exception(
                    u'������ ������������ ������ �� ���� {!r}.'.format(i)
                )
            else:
                available.append(s.portstr)
                s.close()

        return available

    def _create_widget(self):
        """\
            ������������ ��������� ����.
        """
        ralign = QtCore.Qt.AlignRight

        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self._edit_port = QtGui.QComboBox()
        vboxl.addWidget(QtGui.QLabel(u'���:'), alignment=ralign)
        vboxe.addWidget(self._edit_port)
        
        self._edit_baudrate = QtGui.QComboBox()
        vboxl.addWidget(QtGui.QLabel(u'�������� ���/�:'), alignment=ralign)
        vboxe.addWidget(self._edit_baudrate)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        gbox1 = QtGui.QGroupBox(u'��������')
        gbox1.setLayout(hbox)
        
        vboxl = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()
        
        self._edit_bytesize = QtGui.QComboBox()
        vboxl.addWidget(QtGui.QLabel(u'���� ������:'), alignment=ralign)
        vboxe.addWidget(self._edit_bytesize)
        
        self._edit_parity = QtGui.QComboBox()
        vboxl.addWidget(QtGui.QLabel(u'��������:'), alignment=ralign)
        vboxe.addWidget(self._edit_parity)
        
        self._edit_stopbits = QtGui.QComboBox()
        vboxl.addWidget(QtGui.QLabel(u'�������� ����:'), alignment=ralign)
        vboxe.addWidget(self._edit_stopbits)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxe)
        
        gbox2 = QtGui.QGroupBox(u'������ ������')
        gbox2.setLayout(hbox)
        
        self._btn_scan = QtGui.QPushButton(u'��������')
        self.connect(
            self._btn_scan, QtCore.SIGNAL('clicked()'), self._refresh_ports
        )
        
        self._btn_apply = QtGui.QPushButton(u'�������')
        self._btn_apply.clicked.connect(self._set_settings)

        self._btn_abort = QtGui.QPushButton(u'��������')
        self._btn_abort.clicked.connect(self.close)
        
        vboxl = QtGui.QVBoxLayout()
        vboxl.addWidget(gbox1)
        vboxl.addWidget(gbox2)
        
        vboxr = QtGui.QVBoxLayout()
        vboxr.addWidget(self._btn_apply)
        vboxr.addWidget(self._btn_scan)
        vboxr.addWidget(self._btn_abort)
        vboxr.addStretch()

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vboxl)
        hbox.addLayout(vboxr)
        
        self.setLayout(hbox)
        
        # ���������� ����� ��������
        self._edit_port.addItems([str(x) for x in self._scan_ports()])
        self._edit_baudrate.addItems([str(x) for x in serial.Serial.BAUDRATES])
        self._edit_stopbits.addItems([str(x) for x in serial.Serial.STOPBITS])
        self._edit_parity.addItems(
            [str(self.PARITY[x]) for x in serial.Serial.PARITIES]
        )
        self._edit_bytesize.addItems([str(x) for x in serial.Serial.BYTESIZES])

    def set_com(self, data):
        """
            ��������� ������� �� ��������
        """
        self._command = data

    def _protocol(self, char):
        """
            �������� �������� ���� �� ���������.
            ������� ������� ������: 'AA' '31'
        """
        if self._cnt == 0:
            if char == '55':
                self._cnt = 1
        elif self._cnt == 1:
            if char == 'AA':
                self._cnt = 2
            else:
                self._cnt = 0
        elif self._cnt == 2:
            self._com = char
            self._cnt += 1
        elif self._cnt == 3:
            self._length = int(char, 16)
            self._cnt += 1
        else:
            if self._cnt < (5 + self._length - 1):
                self._data.append(char)
                self._cnt += 1
            else:
                if self._check_crc(char):
                    self._bRead = True
                    self.emit(QtCore.SIGNAL("readData(PyQt_PyObject, \
                                            PyQt_PyObject, PyQt_PyObject)"),
                              self._com, self._length, self._data)
                self._cnt = 0

    def _check_crc(self, crc, com=None, length=None, data=None):
        """\
            �������� ����������� CRC (�������� 'AB') � ������������.
            
            ���������� True � ������ ����������
            
            >>> _checkCRC('02', '02', 0, [])
            True
        """

        if com is None:
            com = self._com
        if isinstance(com, str):
            com = int(com, 16)
        val = com
        
        if length is None:
            length = self._length
        if isinstance(length, str):
            length = int(length, 16)
        val += length
        
        if data is None:
            data = self._data
        for x in data:
            if isinstance(x, str):
                x = int(x, 16)
            val += x
        val %= 256
        
        if isinstance(crc, str):
            crc = int(crc, 16)

        return val == crc

    def _cycle_receive(self):
        """\
            ���� ������ ���������
        """
        try:
            tmp = self._port.readall()
        except serial.SerialException:
            # TODO ��������� ���������� ��� ���������� � �����
            tmp = None
         
        # ������� � ������ ������ ������
        if not tmp:
            return

        # ������� ���� ���������� ��������� ��� �� ����������
        if self._bRead:
            return
        
        # ������������ �������� �� ������������ ���������
        for x in tmp:
            self._protocol(x.encode('hex').upper())

    def _cycle_send(self):
        """
            ���� ������ ������� �����������.
        """
        try:
            self._port.write(bytearray.fromhex(self._command))
        except serial.SerialException:
            pass

    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    QtGui.QApplication.setStyle('Cleanlooks')
    
    my_frame = MySerial()
    
    # # �������� �������� ����� � ����������� �� ���������
    my_frame.open_port()
    my_frame.close_port()
    #
    # # �������� �������� ����� � ������� �����������
    # my_frame.set_settings()
    # my_frame.open_port()
    # my_frame.close_port()
    
    my_frame.show()
    app.exec_()
