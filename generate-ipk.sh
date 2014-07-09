#!/bin/bash
# Generate lastest ipk and upload to Github

sdk=/home/paws/openwrt/OpenWrt-SDK-ar71xx-for-Linux-i686-gcc-4.3.3+cs_uClibc-0.9.30.1 # /home/paws/OpenWRT-SDK
pawsrepo=/home/paws/paws-server

cd $sdk

oldversion=0.34
version=0.35

sed -i s/PKG_VERSION:=$oldversion/PKG_VERSION:=$version/g $pawsrepo/Makefile
mkdir -p package/paws
cp $pawsrepo/Makefile package/paws/Makefile
echo "Attempting to generate PAWS ipk $version"
sudo yum install -y ncurses-devel svn
make V=99

cp bin/ar71xx/packages/paws_$version-1_ar71xx.ipk  $pawsrepo/paws-ipk
sudo cp bin/ar71xx/packages/paws_$version-1_ar71xx.ipk  /var/www/html/paws-ipk
echo "If successful, new ipk is avaliable at http://server01.horizon.emnet.co.uk/paws-ipk/paws_$version-1_ar71xx.ipk"

cd $pawsrepo
git add paws-ipk/paws_$version-1_ar71xx.ipk
git add Makefile
git commit -m "adding latest.ipk version $version"
git pull
git push
echo "updating paws-server Github repo has been updated to reflect this change"

echo "-------------------------------------------"
echo "The PAWS ipk version: $version is now avalaible from:"
echo "http://server01.horizon.emnet.co.uk/paws-ipk/paws_$version-1_ar71xx.ipk" 
echo "and (as a backup) https://github.com/pawsnet/paws-server/blob/master/paws-ipk/paws_$version-1_ar71xx.ipk?raw=true"
