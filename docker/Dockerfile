# Dockerfile based on manylinux2014_x86_64
#
# Build with something like this, where
#  -t is the name of the image
#  -f is this file
#  1001 is the UID of the user to run as, you might want to use $UID
#  docker is the directory where install_ffi.sh is
# docker build -t buildslave_x86_64 --build-arg BUILDSLAVE_UID=1001 -f docker/Dockerfile docker 
#
# To create the buildslave configuration, call
# docker run -it --rm -v<abspath/to/builder/dir>:/build_dir \
#    -eSLAVENAME=<name> -ePASSWORD=<password> buildslave_x86_64
# Then you can examine the <build_dir>/buildbot.tac file.
#
# To run the buildslave (after the stage above succeeds) you no longer need the
# SLAVENAME and PASSWORD. The slave will run non-deamonized, which will appear
# to "hang" the console running the slave. To stop the slave, simply CTRL-C or
# kill the process.
#
# Don't forget to `docker container prune` once in a while to reclaim disk
# space from stopped containers.
#
# Use PYPY_MAKE_PORTABLE to package a built PyPy in a portable fashion (that
# is the motivation for doing this in the first place, right?)
#
# docker run -it --rm -v<abspath/to/builder/dir>:/build_dir> \
#     -ePYPY_MAKE_PORTABLE=1 buildslave_x86_64
#
# You might want to keep the TMPDIR where the testing/building
# artifacts are. This will normally be inside the docker, so do something like this
# to save the files outside the docker
#
# mkdir -p build_dir/tmp
# docker run -it --rm -v<abspath/to/builder/dir>:/build_dir> \
#     -eTMPDIR=/build_dir/tmp -ePYPY_MAKE_PORTABLE=1 buildslave_x86_64
#
# To enter the buildslave image, add a shell command to the end
#
# docker run -it -v<abspath/to/builder/dir>:/build_dir> \
#     -eTMPDIR=/build_dir/tmp buildslave_x86_64 /bin/bash
#
# This will enter the docker as root. Don't do "su - buildslave",
# do "su buildslave"

FROM quay.io/pypa/manylinux2014_x86_64:2021-10-26-cf1e11e
WORKDIR /root

RUN yum -y update
RUN yum install -y wget bzip2-devel zlib-devel glibc-devel libX11-devel \
   libXt-devel patch expat-devel libXft-devel tk-devel gdbm-devel gdb vim \
   perl sqlite-devel python-virtualenv libffi-devel libunwind-devel openssl-devel \
   xz-devel
RUN yum -y install perl-IPC-Cmd perl-Digest-SHA  # for OpenSSL3

# Later on openssl files are put in /usr/local/lib64, but expected to be in /usr/local/lib
RUN rm -rf /usr/local/lib64
RUN ln -s /usr/local/lib /usr/local/lib64

# Taken from pyca/infra/cryptography-manylinux
# Use the version of openssl that latests pyca/cryptography uses
ENV PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig:/usr/lib64/pkgconfig
ADD install_openssl.sh /root/install_openssl.sh
RUN sh install_openssl.sh manylinux2014 2>&1 | tee /root/install_openssl.log
# Use an up-to-date version of xz for lzma
ADD install_ncurses.sh /root/install_ncurses.sh
RUN /root/install_ncurses.sh 2>&1 | tee /root/install_ncurses.log
# centos6 provides gc7.1, which does not work in a docker. Use a newer version
# This is for testing only
Add install_gc.sh /root/install_gc.sh
RUN sh /root/install_gc.sh 2>&1 | tee /root/install_gc.log

RUN yum clean packages

# prefer our libraries in /usr/local/lib
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
# but remove broken libcrypt
# RUN rm -rf /usr/local/lib/libcrypt.*

# build python 2.7.18 and link it to a virtualenv
# since centos7 has python2.7.5
RUN wget -q --no-check-certificate http://python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz
RUN tar xf Python-2.7.18.tar.xz
RUN (cd Python-2.7.18 && ./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" && make && make altinstall) > /build_python.log
RUN /usr/local/bin/python2.7 -m ensurepip
RUN /usr/local/bin/python2.7 -m pip install virtualenv
run /usr/local/bin/python2.7 -m virtualenv /python27_virt
ENV PATH=/python27_virt/bin:$PATH
RUN pip install --upgrade pip==20.3.4
RUN pip install --upgrade setuptools
RUN pip install buildbot-slave pytest hypothesis==4.42 cffi mercurial virtualenv pexpect
RUN pip install git+https://github.com/vmprof/vmprof-python.git

# get a pypy for translation.
RUN wget -q --no-check-certificate https://downloads.python.org/pypy/pypy2.7-v7.3.6-linux64.tar.bz2 -O - | tar -C /opt -xj
RUN ln -s /opt/pypy2.7-v7.3.6-linux64/bin/pypy /usr/local/bin/pypy
RUN pypy -mensurepip
RUN pypy -mpip install --upgrade pip==20.3.4
RUN pypy -mpip install --upgrade setuptools wheel

# Remove newer sqlite3 from /usr/local/lib since it does not match the headers
# in /usr/include
RUN rm -rf /usr/local/lib/libsqlite3*

# Define a user
ARG BUILDSLAVE_UID=1001
ARG PARALLEL_BUILDS=4
RUN adduser buildslave --uid=$BUILDSLAVE_UID
RUN echo parallel_runs=$PARALLEL_BUILDS > /home/buildslave/machine_cfg.py

# NOTE: always use
# su buildslave
# not
# su - buildslave
# to preserve env variables
CMD if [ -e /build_dir/buildbot.tac ]; then \
    su buildslave -c "buildslave start --nodaemon /build_dir"; \
  else \
    su buildslave -c "buildslave create-slave /build_dir buildbot.pypy.org:10407 $SLAVENAME $PASSWORD"; \
  fi
