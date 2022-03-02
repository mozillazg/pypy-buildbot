#!/bin/bash
set -xeo pipefail

SQLITE_SHA256=1c76e25dc63d9f3935e0f406aec520a33ee77cf54ea5147dffe1fae8369eff68
SQLITE_VERSION="3380000"

function check_sha256sum {
    local fname=$1
    local sha256=$2
    echo "${sha256}  ${fname}" > "${fname}.sha256"
    sha256sum -c "${fname}.sha256"
    rm "${fname}.sha256"
}

curl -sS -#O "https://sqlite.org/2022/sqlite-autoconf-${SQLITE_VERSION}.tar.gz"
check_sha256sum "sqlite-autoconf-${SQLITE_VERSION}.tar.gz" ${SQLITE_SHA256}
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
