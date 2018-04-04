all: test

.PHONY: test
test: libtcg.o test/simple_loop.bin
	python __init__.py

.PHONY: clean
clean:
	rm -f libtcg.c libtcg.o libtcg.cpython*.so

# Generate Python CFFI interface
libtcg.o: gen_cffi.py $(wildcard inc/*.h)
	python gen_cffi.py

# Assembly test assembly files
%.bin: %.nasm
	nasm -o $@ -l $@.list $<


