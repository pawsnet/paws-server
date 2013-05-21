#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use strict;

print header;
print start_html("Password Change Results");

print qq(<h2>Success 1</h2>\n);
print end_html;



