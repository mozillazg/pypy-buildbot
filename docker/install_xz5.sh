#!/bin/bash
set -xe pipefail
XZ5_FILE=xz-5.2.4.tar.gz

# Let's encrypt's certificate expired Sept 2021, it is difficult to update on
# centos6. When we move to centos7, remove the --no-check-certificate
wget --no-check-certificate -q "https://tukaani.org/xz/${XZ5_FILE}"
gpg --import lasse_collin_pubkey.txt
gpg --verify ${XZ5_FILE}.sig ${XZ5_FILE}

tar zxf ${XZ5_FILE}
pushd xz-5*
if [ "$2" == "m32" ]; then
  setarch i386 ./configure --prefix=/usr/local CFLAGS="-m32"
else
  ./configure --prefix=/usr/local
fi
make install
popd
rm -rf xz-5*
