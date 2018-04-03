pytcg
=====

Status: Very early, but working!  So far it's able to translate from 32-bit x86
to TCG ops and print out some op info. Pythonification is next!

Before using this, you'll need to build libtcg. See the
[libtcg](https://github.com/angr-tcg/qemu) repo.

## Setup

Setup your Python 3 virtual environment with something like:

    sudo apt-get install python3-venv
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

## Run

There's a simple Makefile to build the FFI and run basic interface testing.
