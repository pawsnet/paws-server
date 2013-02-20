#!/bin/bash
# Generate lastest ipk and upload to Github

sdk=/home/paws/OpenWRT-SDK
pawsrepo=/home/paws/paws-server


cd $sdk
oldversion="0.8"
version="0.9"
sed -i 's/PKG_VERSION:=$oldversion/PKG_VERSION:=$version/g' /package/paws/Makefile
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

echo "-------------------------------------------"
echo "The PAWS ipk version: $version is now avalaible from:"
echo "http://server01.horizon.emnet.co.uk/paws-ipk/paws_$version-1_ar71xx.ipk" 
echo "and (as a backup) https://github.com/pawsnet/paws-server/blob/master/paws-ipk/paws_$version-1_ar71xx.ipk?raw=true"
