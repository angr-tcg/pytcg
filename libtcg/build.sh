#!/bin/bash
set -e
QEMU_GIT_REPO="https://github.com/angr-tcg/qemu.git"

if [ ! -d "qemu" ]; then
	echo "[ * ] Cloning libtcg (qemu) repo"
	git clone $QEMU_GIT_REPO qemu
	pushd qemu
	git checkout libtcg
	popd
fi

pushd qemu
if [ ! -d "build" ]; then
	mkdir build
fi
cd build

echo "[ * ] Starting configure"
../configure \
	--target-list=x86_64-libtcg \
	--enable-libtcg \
	--enable-debug \
	--extra-cflags="-g3 -O0" \

echo "[ * ] Building..."
time make -j4 | tee build.log

echo "[ * ] Extracting required files"
popd
cp \
    qemu/build/x86_64-libtcg/libtcg-x86_64.so.2.8.50 \
    qemu/include/libtcg.h \
    qemu/include/tcg-common.h \
    qemu/include/tcg-opc.h \
    .
