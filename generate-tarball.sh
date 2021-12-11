#!/bin/sh

set -e

GIT_TAG='4.2.3'
VERSION="$(sed -n 's/Version:\s*//p' *.spec)"

# Retrieve and set version
git clone https://github.com/angband/angband.git
 
pushd angband
git reset --hard "${GIT_TAG}"

# Remove restricted assets
## Shockbolt tileset aren't distributed under a valid license
rm -rf lib/tiles/shockbolt

## Sound files aren't distributed under a valid license
rm -rf lib/sounds/*

## Windows library headers aren't distributed under a valid license
rm -rf src/cocoa
rm -rf src/nds
rm -rf src/win

## Clean up
git apply ../fix-restricted.patch

rm -rf .git
popd

mv angband angband-$VERSION
tar -czvf angband-$VERSION-norestricted.tar.gz angband-$VERSION
rm -rf angband-$VERSION
