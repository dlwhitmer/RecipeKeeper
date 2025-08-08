# -*- mode: python; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['recipe_keeper.py'],
    pathex=['.'],                # look in this folder for all inputs
    binaries=[],
    datas=[ ('Recipe_keeper.db', '.'), ('book.ico', '.') ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,      # let COLLECT gather binaries+datas
    name='recipe_keeper',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='book.ico',             # embed this single ICO file
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Recipe Keeper',
)
