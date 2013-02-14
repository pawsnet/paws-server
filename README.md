## How to use PAWS Router Management Server

To get set-up and ready to remotely manage the PAWS routers: Get access to the Management Server as PAWS user and move to the correct directory to run the management scripts

	$ ssh -i <privatekey> <username>@server01.horizon.emnet.co.uk
	$ sudo su paws
	$ cd /home/paws/paws-server/scripts/

Now you can do the following things:

Get a list of currently connected PAWS routers

	$ ./bdm list 

SSH into a particular PAWS router 

	$ ./bdm console <device-ID>

Enable/disable Wifi on a particular PAWS router

	$ ./bdm config   <dev_id> [wifi-enable/wifi-disable]

Enable/disable throttling on a particular PAWS router

	$ config   <dev_id> [throttle/remove-throttle]



## PAWS Router Management Server Instruction 

(for Ubuntu NOT CentOS)
Acknowledgements: Original source from https://github.com/projectbismark 
Modified for PAWS by Arjuna Sathiaseelan: arjuna.sathiaseelan@cl.cam.ac.uk

Server Installation Instructions
--------------------------------
1) Get code from github

	$ sudo apt-get update
	$ sudo apt-get install git
	$ mkdir paws-server
	$ mkdir etc
	$ git clone https://github.com/pawsnet/paws-server.git

(2) postgresql Installation process

	$ sudo apt-get install sqlite3 postgresql
	$ cd paws-server/conf
	$ cp * ../../etc/

(3) adding "paws" as a database user

	$ sudo su - postgres
	$ psql -U postgres
	CREATE USER paws PASSWORD 'paws123';
	ALTER USER paws WITH SUPERUSER CREATEDB CREATEROLE;

\du to see user lists
\l to see list of all databases
^Z for exiting psql

(4) database authentication

	$ sudo updatedb
	$ locate pg_hba.conf

	$ vim <directory-from-above>

set all authentication to trust

(5) Restart postgresql and setup database from paws user

	$ /etc/init.d/postgresql restart

To go back to user paws

	$ logout

go to db directory

	$ cd ~/paws-server/db
	$ ./bdm_db.sh create_db
	$ ./bdm_db.sh create_tables


(6) Python Installation

Note: bdmd/mkvirtualenv.sh is deprecated - so lets do a manual installation

	$ cd ../bdmd
	$ sudo apt-get install python-pip python-dev build-essential
	$ sudo pip install --upgrade pip
	$ sudo pip install --upgrade virtualenv
	$ which virtualenv
    		 -> $dir/virtualenv
	$ <dir-from-above>/virtualenv --no-site-packages --distribute virt-python
	$ source virt-python/bin/activate
	$ pip install --ignore-installed --install-option="--prefix=/home/paws/paws-server/bdmd/virt-python" txpostgres
	
( for the following to work i needed to add) sudo apt-get install
postgresql-server-dev-all)

	$ pip install --ignore-installed --install-option="--prefix=/home/paws/paws-server/bdmd/virt-python" psycopg2
	$ pip install --ignore-installed --install-option="--prefix=/home/paws/paws-server/bdmd/virt-python" twisted

	$ cd ../scripts
	$ ./bdmd start


bdm script to play around with the routers (to list, to create tunnels, to open console, to enabe/disable paws wifi, to throttle
rates, to do updates to script, configs, packages).


