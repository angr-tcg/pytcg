#!/bin/bash
set -e
QEMU_GIT_REPO="https://github.com/angr-tcg/qemu.git"

echo "[ * ] Cloning libtcg (qemu) repo"
git clone $QEMU_GIT_REPO qemu
pushd qemu
git checkout libtcg
mkdir build && cd build

echo "[ * ] Starting configure"
../configure --target-list=x86_64-libtcg --enable-libtcg

echo "[ * ] Building..."
make

echo "[ * ] Extracting required files"
popd
cp \
    qemu/build/x86_64-libtcg/libtcg-x86_64.so.2.8.50 \
    qemu/include/libtcg.h \
    qemu/include/tcg-common.h \
    qemu/include/tcg-opc.h \
    .
