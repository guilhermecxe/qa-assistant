# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('chromadb', include_py_files=True, includes=['**/*.py', '**/*.sql'])

block_cipher = None

a = Analysis(
    ['app\\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'chromadb.telemetry.product.posthog',
        'chromadb.api.segment',
        'chromadb.db.impl',
        'chromadb.db.impl.sqlite',
        'chromadb.migrations',
        'chromadb.migrations.embeddings_queue',
        'hnswlib',
        'langchain.chains.history_aware_retriever',
        'langchain.chains.retrieval',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts, 
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas, 
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main')
