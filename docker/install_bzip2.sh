#!/bin/bash
set -xeo pipefail

BZIP2_VERSION="1.0.8"

function check_sha256sum {
    local fname=$1
    local sha256=$2
    echo "${sha256}  ${fname}" > "${fname}.sha256"
    sha256sum -c "${fname}.sha256"
    rm "${fname}.sha256"
}

wget https://sourceware.org/pub/bzip2/bzip2-${BZIP2_VERSION}.tar.gz
tar zxf bzip2*.tar.gz
pushd bzip2*
CONFIGURE_PRE="--prefix=/usr/local --enable-shared=yes --enable-static=yes --disable-dependency-tracking"
CFLAGS="-fPIC ${CFLAGS}"
if [ "$1" == "m32" ]; then
  setarch i386 ./configure ${CONFIGURE_PRE} CFLAGS="-m32 ${CFLAGS}"
else
  ./configure ${CONFIGURE_PRE} CFLAGS=${CFLAGS}
fi
make install
popd
rm -rf bzip2*
