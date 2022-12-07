#!/bin/bash
set -xeo pipefail

function check_sha256sum {
    local fname=$1
    local sha256=$2
    echo "${sha256}  ${fname}" > "${fname}.sha256"
    sha256sum -c "${fname}.sha256"
    rm "${fname}.sha256"
}

wget https://github.com/libexpat/libexpat/releases/download/R_2_5_0/expat-2.5.0.tar.gz
tar zxf expat*.tar.gz
pushd expat*
CONFIGURE_PRE="--prefix=/usr/local --enable-shared=yes --enable-static=yes --disable-dependency-tracking"
CFLAGS="-fPIC ${CFLAGS}"
if [ "$1" == "m32" ]; then
  setarch i386 ./configure ${CONFIGURE_PRE} CFLAGS="-m32 ${CFLAGS}"
else
  ./configure ${CONFIGURE_PRE} CFLAGS=${CFLAGS}
fi
make install
popd
rm -rf expat*
