.PHONY: all

objects := main.o

all: sml2.gb

%.o: %.asm
	rgbasm -o $@ $<

sml2.gb: $(objects)
	rgblink -n ml2.sym -o $@ $^
	rgbfix -v $@
	c:/src/archipelago/venv/scripts/python.exe extractor.py
	rm -f main.o