FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python-software-properties \
    software-properties-common \
 && add-apt-repository ppa:chris-lea/libsodium \
 && echo "deb http://ppa.launchpad.net/chris-lea/libsodium/ubuntu trusty main" >> /etc/apt/sources.list \
 && echo "deb-src http://ppa.launchpad.net/chris-lea/libsodium/ubuntu trusty main" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y libsodium-dev python-pip

RUN pip install Hummingbird

ENTRYPOINT ["/usr/local/bin/Hummingbird"]

# usage:
# docker run -d --restart=always -p 1314:1314 ficapy/hummingbird -s 0.0.0.0 -p 1314 -k $PD -m chacha20
