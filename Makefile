all: test

libtcg.o: gen_cffi.py
	python gen_cffi.py

%.bin: %.nasm
	nasm -o $@ -l $@.list $<

.PHONY: clean
clean:
	rm -f libtcg.c libtcg.o libtcg.cpython*.so

.PHONY: test
test: libtcg.o test/simple_loop.bin
	python __init__.py
