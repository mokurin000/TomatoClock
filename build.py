import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "src/tomatoclock/__main__.py",
        "--noconfirm",
        "--windowed",
        "--name=TomatoClock",
        "--noconsole",
        "--optimize=2",
        "--collect-data=tomatoclock",
        "--icon=./src/tomatoclock/tomato.ico",
    ]
)
