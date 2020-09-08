set -eux

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get -y upgrade
apt-get -y install --no-install-recommends \
    gcc \
    libcurl4-openssl-dev \
    libmemcached-dev \
    libpq-dev \
    libssl-dev \
    libz-dev \
    netcat
apt-get clean
rm -rf /var/lib/apt/lists/*
