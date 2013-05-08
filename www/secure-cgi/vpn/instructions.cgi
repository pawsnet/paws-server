#!/usr/bin/perl -wT


use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

print header;

print start_html(
        -title  =>      'PAWS VPN Instructions',
        -style  =>      {'src'  =>      '/styles/style.css'},
);
print img { src => "/images/pawshdrmid.png", align => "CENTER" };


#foreach my $key (sort(keys(%ENV))) {
	#print "$key = $ENV{$key}<br>\n";
#}

my $agent;

#$agent='Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25';
#$agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31';

$agent=$ENV{'HTTP_USER_AGENT'};

print "<hr><p>";
print $agent;
print "<hr><p>";

#if ( $ENV{'HTTP_USER_AGENT'} =~ /NT\s(\d\.\d)/ ) {
#	print $1;
#}

if ( $agent =~ /Android\s(\d)\.(\d)\.(\d)/ ) {
	my $android_v1 = $1;
	my $android_v2 = $2;
	my $android_v3 = $3;


	print("<H2>You appear to be using Android $android_v1.$android_v2.$android_v3</H2>");
	print("<p>Please follow the instructions below to configure your VPN client:</p>");

	print_android_2_l2tp();
	#if ($android_v1 <= 3) {
	#	print_android_2_l2tp();
	#}
	#else {
	#	print_android_4_pptp();
	#}
}
elsif ( $agent =~ /\((iP\w+);/ ) {
	print("<H2>You appear to be using $1</H2>");
	print("<p>Please follow the instructions below to configure your VPN client:</p>");
	print_iphone_l2tp();
}
elsif ( $agent =~ /Macintosh;.*Mac (OS\s+X\s+\d+_\d+_\d+)/ ) {
	print("<H2>You appear to be using $1</H2>");
	print("<p>Please follow the instructions below to configure your VPN client:</p>");
	print_apple_l2tp();
}
elsif ( $agent =~ /Windows\sNT/ ) {
	print("<H2>You appear to be using Microsoft Windows</H2>");
	print("<p>Please follow the instructions below to configure your VPN client:</p>");
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

	print <<ANDROID_2_L2TP;

	<ul>
	
	<li>
        	Open Settings and click on Wireless Controls
	</li>
	<li>
        	Click on VPN Settings
	</li>
	<li>
        	Click on Add VPN
	</li>
	<li>
        	Choose L2TP/IPSec PSK VPN
	</li>
	<li>
        	In the VPN Name field, enter &quot;<b>PAWS L2TP</b>&quot;
	</li>
	<li>
        	In the Set VPN Server field enter &quot;<b>83.223.208.50</b>&quot;
	</li>
	<li>
        	Set IPSec pre-shared key to &quot;<b>S3cr3t4PAWSPr0j3ct</b>&quot;. Please do NOT share this with anyone!
	</li>
	<li>
        	Do NOT enable L2TP secret.
	</li>
	<li>
        	Click Save or Back
	</li>
	<li>
	</ul>

	<ul>
	<li>
        Open Settings and click on Wireless Controls
	</li>
	<li>
        Click on &quot;<b>PAWS L2TP</b>&quot;
	</li>
	<li>
        In the Username: field, enter your  username
	</li>
	<li>
        In the Password: field, enter your password
	</li>
	<li>
        Click Connect
	</li>



	</ul>

ANDROID_2_L2TP

}

#########################
sub print_iphone_l2tp {

	print <<IPHONE_L2TP;

	<ul>
	<li>
	Choose &quot;Settings&quot; from your  home screen.
	</li>
	<li>
	Choose &quot;General&quot;
	</li>
	<li>
	Choose &quot;Network&quot;
	</li>
	<li>
	Choose &quot;VPN&quot;
	</li>
	<li>
	Choose &quot;Add VPN Configuration&quot;
	</li>
	<li>
	Choose &quot;L2TP&quot;
	</li>
	<li>
	Description = &quot;<b>PAWS L2TP</b>&quot;
	</li>
	<li>
	Server: &quot;<b>83.223.208.50</b>&quot;
	</li>
	<li>
	Account: Enter your PAWS username
	</li>
	<li>
	RSA SecurID: OFF
	</li>
	<li>
	Password: Your PAWS password
	</li>
	<li>
	Secret: &quot;<b>S3cr3t4PAWSPr0j3ct</b>&quot;
	</li>
	<li>
	Send all Traffic: ON
	</li>
	<li>

	Click SAVE at the top
	</li>
	<li>


	Go back to VPN screen found at:
	</li>
	<li>

	Settings -> General -> Network -> VPN or Settings ->VPN and slide selector to ON.
	</li>

	</ul>

IPHONE_L2TP

}
#########################
sub print_windows {

	print <<WINDOWS_L2TP;

        <ul>
        <li>
	Click on Windows Start Orb (bottom left corner)
	</li>
        <li>
	Click on Control Panel
	</li>
        <li>
	Click on Network and Internet
	</li>
        <li>
	Click on Network and Sharing CenterYour screen should look similar to this
	</li>
        <li>
	Click on Setup a new connection or network
	</li>
        <li>
	Choose Use My Internet Connection
	</li>
        <li>

	Input your settings:
	</li>
        <li>
	Internet Address: &quot;<b>83.223.208.50</b>&quot;
	</li>
        <li>
	Destination Name: &quot;<b>PAWS L2TP</b>&quot;
	</li>
        <li>
	IMPORTANT: Click on the option Dont connect now; just set it up so I can connect later
	</li>
        <li>

	Click Next
	</li>
        <li>
	Input your PPTP Username and Password
	</li>
        <li>
	Click Create
	</li>
        <li>
	IMPORTANT Click on CLOSE (do not connect right now or it will fail)
	</li>
        <li>
	Click Connect to a network now that you are back at the Network and Sharing Center
	</li>
        <li>
	On the pop-up window double click the &quot;<b>PAWS L2TP</b>&quot; name
	</li>
        <li>
	Click on Properties
	</li>
        <li>
	Click on Options
	</li>
        <li>
	Uncheck Include Windows logon domain
	</li>
        <li>
	Click on Security
	</li>
        <li>
	On Type of VPN Choose L2TP/IPSec
	</li>
        <li>
	Click on the Advanced button
	</li>
        <li>
	Click on the top option Use preshared key for authentication
	</li>
        <li>
	Input &quot;<b>S3cr3t4PAWSPr0j3ct</b>&quot; as the Key
	</li>
        <li>
	Click Ok
	</li>
        <li>
	Click on Networking
	</li>
        <li>
	Uncheck Internet Protocol Version 6
	</li>
        <li>
	Click OK
	</li>
        <li>
	On the connect screen enter your username and password again
	</li>
        <li>
	Click on Connect
	</li>
        <li>
	You should be connected to the VPN now.
	</li>
        </ul>



WINDOWS_L2TP

}
#########################
sub print_apple_l2tp {

	print <<APPLE_L2TP;

	<ul>

	<li>
	To setup the connection, you need to create a new connection profile in your network preferences.
	</li>
	<li>
	Click on Apple
	</li>
	<li>
	System Preferences
	</li>
	<li>
	Network Icon
	</li>
	<li>
	Click the + sign in the lower left corner
	</li>
	<li>
	When you click the + sign, a window will pop up. On the INTERFACE dropdown choose VPN
	</li>
	<li>

	VPN TYPE: L2TP over IPSec 
	</li>
	<li>


	Click Create
	</li>
	<li>
	Server Address: &quot;<b>83.223.208.50</b>&quot;
	</li>
	<li>
	Account Name: Enter your PAWS username
	</li>
	<li>

	Click on Authentication Settings
	</li>
	<li>
	In the pop-up click on Password and put in your password
	</li>
	<li>
	Click on Shared Secret and put in &quot;<b>S3cr3t4PAWSPr0j3ct</b>&quot; as the shared secret
	</li>
	<li>
	Click OK
	</li>
	<li>
	DO NOT CLICK CONNECT YET
	</li>
	<li>
	Click on Advanced
	</li>
	<li>
	Click on the option send all traffic over VPN connection
	</li>
	<li>
	Click Ok
	</li>
	<li>

	Click Apply
	</li>
	<li>

	Your L2TP connection is setup now. Click on Connect
	</li>

	<ul>

APPLE_L2TP

}

#########################
sub print_unknown {

	print "<br>\n";
	print "Instructions for this device coming soon...\n";
	print "<br>\n";

}

