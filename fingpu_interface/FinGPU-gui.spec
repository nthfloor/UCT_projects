# -*- mode: python -*-
a = Analysis(['runapp.py'],
             pathex=['/home/nathanf/Repo/uct_projects/fingpu_interface'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FinGPU-gui',
          debug=False,
          strip=None,
          upx=True,
          console=True )
