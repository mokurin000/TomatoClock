import PyInstaller.__main__

PyInstaller.__main__.run(
    ["tomato.py", "--onefile", "--windowed", "--name=TomatoClock", "--noconsole"]
)
