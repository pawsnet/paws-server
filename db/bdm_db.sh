#!/bin/bash

set -o nounset  # Don't allow uninitialized variables to be used
set -o errexit  # Die if a function returns non-zero

source ~/etc/bdm_db.conf

default_BDM_PG_HOST='127.0.0.1'
default_BDM_PG_PORT='5432'
default_BDM_PG_MGMT_DBNAME='paws_mgmt'
default_BDM_PG_USER='paws'

BDM_PG_HOST=${BDM_PG_HOST:-$default_BDM_PG_HOST}
BDM_PG_PORT=${BDM_PG_PORT:-$default_BDM_PG_PORT}
BDM_PG_MGMT_DBNAME=${BDM_PG_MGMT_DBNAME:-$default_BDM_PG_MGMT_DBNAME}
BDM_PG_USER=${BDM_PG_USER:-$default_BDM_PG_USER}

psqlcmd="psql -U $BDM_PG_USER -h $BDM_PG_HOST -p $BDM_PG_PORT"
psqlcmd_db="$psqlcmd -d $BDM_PG_MGMT_DBNAME"

function connect_or_die()
{
    if ! $($psqlcmd -l &>/dev/null); then
        echo "Cannot connect to postgres. Check connection parameters."
        exit 1
    fi
}

function db_exists()
{
    connect_or_die
    [ "$($psqlcmd -l 2>/dev/null | grep -c $BDM_PG_MGMT_DBNAME)" -ne 0 ]
}

function tables_exist()
{
    db_exists && \
        [ $($psqlcmd_db -A -q -t -c '\dt' 2>/dev/null | wc -l) -ne 0 ]
}

function db_exists_or_die()
{
    if ! db_exists; then
        echo "Database '$BDM_PG_MGMT_DBNAME' does not exist."
        echo "Run '$0 create_db' to create the database."
        exit 1
    fi
}

function tables_exist_or_die()
{
    if ! tables_exist; then
        echo "The necessary tables in '$BDM_PG_MGMT_DBNAME' do not exist."
        echo "Run '$0 create_tables' to create the tables."
        exit 1
    fi
}

function help()
{
    echo "usage: $0 {create_db|create_tables|drop_db|drop_tables}"
}

if [ ${1:-'1_is_unset'} = '1_is_unset' ]; then
    help
    exit
fi

case $1 in
create_db)
    if ! db_exists; then
        createdb $BDM_PG_MGMT_DBNAME
    else
        echo "Database '$BDM_PG_MGMT_DBNAME' already exists."
    fi
;;
create_tables)
    db_exists_or_die
    if ! tables_exist; then
        $psqlcmd_db -f paws_mgmt_functions.sql
        $psqlcmd_db -f paws_mgmt_tables.sql
    else
        echo "There are already tables in '$BDM_PG_MGMT_DBNAME'."
    fi
;;
drop_tables)
    if tables_exist; then
        echo "I'm not willing to do this automatically, Arjuna."
        echo -n "Try running: $psqlcmd_db"
        echo " -c 'DROP SCHEMA public CASCADE;'"
    else
        echo "There are no tables in '$BDM_PG_MGMT_DBNAME'."
    fi
;;
drop_db)
    if db_exists; then
        echo "I'm not willing to do this automatically,Arjuna."
        echo -n "Try running: $psqlcmd"
        echo " -c 'DROP DATABASE $BDM_PG_MGMT_DBNAME;'"
    else
        echo "Database '$BDM_PG_MGMT_DBNAME' does not exist."
    fi
;;
db_exists)
    if db_exists; then
        exit 0
    else
        exit 1
    fi
;;
tables_exist)
    if tables_exist; then
        exit 0
    else
        exit 1
    fi
;;
*)
    help
;;
esac
