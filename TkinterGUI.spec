# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TkinterGUI.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pkg_resources', 'pkg_resources.py2_warn', 'pkg_resources.extern', 'cryptography.hazmat.primitives.kdf.pbkdf2', 'pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.timestamps', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.period', 'pandas._libs.tslibs.timezones', 'pandas._libs', 'pandas._libs.parsers', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.hashtable', 'pandas._libs.sparse', 'pandas._libs.json', 'pandas._libs.lib', 'pandas._libs.window'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TkinterGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
