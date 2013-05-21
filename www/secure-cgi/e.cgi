#!/usr/bin/perl -wT
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

print header;
print start_html("Environment");

#foreach my $key (sort(keys(%ENV))) {
	#print "$key = $ENV{$key}<br>\n";
#}

print "<hr><p>";
print $ENV{'HTTP_USER_AGENT'};
print "<hr><p>";

#if ( $ENV{'HTTP_USER_AGENT'} =~ /NT\s(\d\.\d)/ ) {
#	print $1;
#}

if ( $ENV{'HTTP_USER_AGENT'} =~ /Android\s(\d)\.(\d)\.(\d)/ ) {
	my $android_v1 = $1;
	my $android_v2 = $2;
	my $android_v3 = $3;


	print("<H2>You appear to be using Android $android_v1.$android_v2.$android_v3</H2>");
	print("<p>Please follow the instructions below to configure your VPN client:</p>");

	if ($android_v1 <= 3) {
		print_android_2_l2tp();
	}
	else {
		print_android_4_pptp();
	}
}
elsif ( $ENV{'HTTP_USER_AGENT'} =~ /Windows\sNT/ ) {
		print_windows();
}
else {
		print_unknown();
}

print end_html;



#########################
sub print_android_4_pptp {

	print "<br>\n";
	print "Android PPPP\n";
	print "<br>\n";

}
#########################
sub print_android_2_l2tp {

	print "<br>\n";
	print "Android L2TP\n";
	print "<br>\n";

}

#########################
sub print_iphone_l2tp {

	print "<br>\n";
	print "Android L2TP\n";
	print "<br>\n";

}
#########################
sub print_windows {

	print "<br>\n";
	print "Windows\n";
	print "<br>\n";

}
#########################
sub print_unknown {

	print "<br>\n";
	print "Instructions for this device coming soon...\n";
	print "<br>\n";

}

