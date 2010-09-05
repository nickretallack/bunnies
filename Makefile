all:
	rm dist/*
	python setup.py py2exe
	mv dist/main.exe dist/bunnies.exe
	zip dist/bunnies.zip dist/bunnies.exe
