pytcg
=====

Status: Very early, but working!  So far it's able to translate from 32-bit x86
to TCG ops and print out some op info. Pythonification is next!

## Build libtcg

Before using pytcg, you'll need to build libtcg. You can do this by:

    cd libtcg
    ./build.sh

This will clone the Qemu repository with the libtcg patches, build, and extract
the necessary files into this directory.

See the [libtcg](https://github.com/angr-tcg/qemu) repo for more info.

## Setup Python 3 Virtual Environment

Setup your Python 3 virtual environment with something like:

    sudo apt-get install python3-venv
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

## Run

There's a simple Makefile to build the FFI and run basic interface testing.
