import sys
from cx_Freeze import setup, Executable

setup(
    name = "Grumpy Token",
    version = "0.9b",
    description = "Command line interface to grumpy token framework",
    executables = [Executable("wheel.py", base = None)])
