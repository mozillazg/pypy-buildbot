#!/bin/bash
set -xeo pipefail

SQLITE_SHA3=efb103ff4406a2217fa6147e8b88ba54f6c5582e83ef4ff2840be2b306d8172b
SQLITE_VERSION="3380200"

function check_sha3 {
    local fname=$1
    local sha3_in=$2
    local sha3_file=$(openssl dgst -sha3-256 -r $fname |cut -d* -f1)
    if [ "$sha3_file" != "$sha3_in " ]; then  # extra " " is on purpose
        echo "sha3 mismatch"
        exit 1
    fi
}

curl -sS -#O "https://sqlite.org/2022/sqlite-autoconf-${SQLITE_VERSION}.tar.gz"
check_sha3 "sqlite-autoconf-${SQLITE_VERSION}.tar.gz" ${SQLITE_SHA3}
tar zxf sqlite*.tar.gz
pushd sqlite*
CFLAGS="-Os -fPIC -DSQLITE_ENABLE_FTS5 -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_JSON1 -DSQLITE_ENABLE_RTREE -DSQLITE_TCL=0"
CONFIGURE_PRE="--prefix=/usr/local --enable-threadsafe --enable-shared=yes --enable-static=yes --disable-readline --disable-dependency-tracking"
if [ "$1" == "m32" ]; then
  setarch i386 ./configure ${CONFIGURE_PRE} CFLAGS="-m32 ${CFLAGS}"
else
  ./configure ${CONFIGURE_PRE} CFLAGS="${CFLAGS}"
fi
make install
popd
rm -rf sqlite*
