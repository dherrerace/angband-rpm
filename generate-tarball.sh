#!/bin/sh

VERSION=$1

tar -xzvf angband-${VERSION}.tar.gz
rm -rf angband-${VERSION}/lib/tiles/shockbolt

sed -ie 's/shockbolt//' angband-${VERSION}/lib/tiles/Makefile
sed -ie '/name:5:Shockbolt/,$d' angband-${VERSION}/lib/tiles/list.txt

tar -czvf angband-$VERSION-noshockbolt.tar.gz angband-$VERSION
