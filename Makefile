all: test

libtcg.o: build_cffi.py
	python build_cffi.py

test_asm.bin: test_asm.nasm
	nasm -o $@ $<

.PHONY: clean
clean:
	rm -f libtcg.c libtcg.o libtcg.cpython*.so

.PHONY: test
test: libtcg.o test_asm.bin
	python test_cffi.py
