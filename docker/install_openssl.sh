#!/bin/bash
set -xeo pipefail

OPENSSL_URL="https://www.openssl.org/source/"
OPENSSL_NAME="openssl-1.1.1m"
OPENSSL_SHA256="f89199be8b23ca45fc7cb9f1d8d3ee67312318286ad030f5316aca6462db6c96"

function check_sha256sum {
    local fname=$1
    local sha256=$2
    echo "${sha256}  ${fname}" > "${fname}.sha256"
    sha256sum -c "${fname}.sha256"
    rm "${fname}.sha256"
}

echo args are $1 $2

curl -sS -#O "${OPENSSL_URL}/${OPENSSL_NAME}.tar.gz"
check_sha256sum ${OPENSSL_NAME}.tar.gz ${OPENSSL_SHA256}
tar zxf ${OPENSSL_NAME}.tar.gz
PATH=/opt/perl/bin:$PATH
pushd ${OPENSSL_NAME}
if [ "$2" == "m32" ]; then
  setarch i386 ./Configure no-comp no-shared no-dynamic-engine -m32 linux-generic32 --prefix=/usr/local --openssldir=/usr/local
else
  ./config no-comp enable-ec_nistp_64_gcc_128 no-shared no-dynamic-engine --prefix=/usr/local --openssldir=/usr/local
fi
make depend
make -j4
# avoid installing the docs
# https://github.com/openssl/openssl/issues/6685#issuecomment-403838728
make install_sw install_ssldirs
popd
rm -rf openssl*
