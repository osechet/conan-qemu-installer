#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install cmake || true

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv install 3.7.1
    pyenv virtualenv 3.7.1 conan
    pyenv rehash
    pyenv activate conan
else
    sudo apt-get install -y build-essential zlib1g-dev pkg-config libglib2.0-dev binutils-dev \
        libboost-all-dev autoconf libtool libssl-dev libpixman-1-dev
fi

wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
pip install conan_package_tools # It install conan too
conan user
