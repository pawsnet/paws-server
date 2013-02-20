#!/bin/bash
# Generate lastest ipk and upload to Github

version="0.8"
sdk=/home/paws/OpenWRT-SDK
pawsrepo=/home/paws/paws-server

cd $sdk
vi package/paws/Makefile
make V=99
echo "PAWS ipk $version has been successfully generated"

cp bin/ar71xx/packages/paws_$version-1_ar71xx.ipk  $pawsrepo
sudo cp bin/ar71xx/packages/paws_$version-1_ar71xx.ipk  /var/www/html/paws-ipk
echo "The new ipk is avaliable at http://server01.horizon.emnet.co.uk/paws-ipk/paws_$version-1_ar71xx.ipk"

cp package/paws/Makefile $pawsrepo
cd $pawsrepo
git add paws_$version-1_ar71xx.ipk
git add Makefile
git commit -m "adding latest.ipk version $version"
git pull
git push
echo "paws-server Github repo has been updated to reflect this change"

`
