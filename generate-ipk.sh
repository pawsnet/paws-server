#!/bin/bash
# Generate lastest ipk and upload to Github

version="0.8"
sdk=/home/paws/OpenWRT-SDK
pawsrepo=~/home/paws/paws-server

cd $sdk
vim package/paws/Makefile
make V=99
cp bin/ar71xx/packages/paws_$version-1_ar71xx.ipk  $pawsrepo
cp package/paws/Makefile $pawsrepo
cd $pawsrepo
git add paws_$version-1_ar71xx.ipk
git add Makefile
git commit -m "adding latest.ipk version $version"
git pull
git push


