from setuptools import setup, find_packages
import py2exe

setup(
    name = "Bunnies",
    version = "0.1",
    packages = find_packages(),
    windows=[
            {'script': 'main.py',
             #'icon_resources': [(1, 'moduleicon.ico')]
            }
    ],
    zipfile=None,
    options={'py2exe':{
        'bundle_files': 1
    }}
)
