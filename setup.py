# -*- coding: utf-8 -*-
# ��� ������� � ��������� ������ ��������: setup.py py2exe
import sys
from distutils.core import setup
from glob import glob
import py2exe

# ����������� ��������� Visual Studio
sys.path.append("D:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'D:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
# ����������� ����� ������
mydata_files = ('', ["MkUM.dat"])
data_files.append(mydata_files)

includes = ["sip"]
excludes = ['w9xpopen.exe']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll', 'w9xpopen.exe']

setup(
	# ����������� ��������� Visual Studio
	data_files=data_files,
	#w9xpopen.exe - ��� ������������� � win 95/98
	#dll_excludes=['w9xpopen.exe'],
	# windows - GUI (����� ���� console)
	# icon_resources -> ��������� ������ ��� ����������������� �������
    windows=[{"script":"mkum.py", "icon_resources": [(1, "Apps_24x24.ico")]}],
	#
    #options={"py2exe": {"includes":["sip"]}}
	options = {"py2exe": {"compressed": 2, 
						  "optimize": 2,
						  "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
	zipfile=None
)
