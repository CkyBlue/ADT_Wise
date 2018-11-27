# -*- mode: python -*-
#------------------
from kivy.deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all
#------------------
block_cipher = None
""" 
#Add the following to your scripts and use the return as the path to be used

import os, sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
"""
a = Analysis(['main.py'],
             pathex=['G:\\Project\\Programming\\Current Projects\\Prj_06 (ADT-Wise)\\Pass I'],
             binaries=[],
             datas=[("insertionSort_pseudo.txt", ".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='beeper',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
