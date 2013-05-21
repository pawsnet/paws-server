#!/usr/bin/perl

# mvr
# script to parse PAWS users VPN traffic statistics and visited URLs
# Version: 0.1

use Data::Dumper;
use Digest::MD5 qw(md5 md5_hex md5_base64);

my %sessions;

my $sor =0;
my $eor =0;

my $cnt=0;
while (<>) {


	if (/^\w/) {
		$User_Name = "";
        	$Acct_Status_Type = "";
        	$Calling_Station_Id = "";
        	$Framed_IP_Address = "";
        	$NAS_IP_Address = "";
        	$Acct_Unique_Session_Id = "";
        	$Timestamp_Start = "";

        	$Acct_Session_Time = "";
        	$Acct_Output_Octets = "";
        	$Acct_Input_Octets = "";
        	$Acct_Terminate_Cause = "";
        	$Timestamp_Stop = "";

		#print "\n\n====================== \n";
		#print "START \n";
		#print "====================== \n";
	}

	if ( /User-Name = "(\w+)"/ ) {
		#print "$_\n";
		$User_Name = $1;

		#print $User_name, "\n";
	}
	if ( /Acct-Status-Type = (\w+)/ ) {
		#print "$_\n";
		$Acct_Status_Type = $1;

		#print $Acct_Status_Type, "\n";
	}
	if ( /Calling-Station-Id = "(\d+\.\d+.\d+.\d+)"/ ) {
		#print "$_\n";
		$Calling_Station_Id = $1;

		#print $Calling_Station_Id, "\n";
	}
	if ( /Framed-IP-Address = (\d+\.\d+.\d+.\d+)/ ) {
		#print "$_\n";
		$Framed_IP_Address = $1;

		#print $Framed_IP_Address, "\n";
	}
	if ( /NAS-IP-Address = (\d+\.\d+.\d+.\d+)/ ) {
		#print "$_\n";
		$NAS_IP_Address = $1;


		#print $NAS_IP_Address, "\n";
	}
	if ( /Acct-Unique-Session-Id = "(\w+)"/ ) {
		#print "$_\n";
		$Acct_Unique_Session_Id = $1;
		#print $Acct_Unique_Session_Id, "\n";
	}
	if ( /Timestamp = (\d+)/ ) {
		#print "$_\n";
		$my_tmp_ts = $1;
		#print $my_tmp_ts, "\n";
		if ( $Acct_Status_Type eq "Start" ) {
			$Timestamp_Start = $my_tmp_ts;
		}
		else  {
			$Timestamp_Stop = $my_tmp_ts;
		}
	}
	if ( /Acct-Session-Time = (\d+)/ ) {
		#print "$_\n";
		$Acct_Session_Time = $1;
		#print $Acct_Session_Time, "\n";
	}
	if ( /Acct-Output-Octets = (\d+)/ ) {
		#print "$_\n";
		$Acct_Output_Octets = $1;
		#print $Acct_Output_Octets, "\n";
	}
	if ( /Acct-Input-Octets = (\d+)/ ) {
		#print "$_\n";
		$Acct_Input_Octets = $1;
		#print $Acct_Input_Octets, "\n";
	}
	if ( /Acct-Terminate-Cause = (\S+)/ ) {
		#print "$_\n";
		$Acct_Terminate_Cause = $1;
		#print $Acct_Terminate_Cause, "\n";
	}

	if (/^$/) {
		$eor=1;
		#print "=============================\n";
		#print;

		$sessions{$Acct_Unique_Session_Id}{'User-Name'} = $User_Name;
		$sessions{$Acct_Unique_Session_Id}{'Calling-Station-Id'} = $Calling_Station_Id;
		$sessions{$Acct_Unique_Session_Id}{'Framed-IP-Address'} = $Framed_IP_Address;
		$sessions{$Acct_Unique_Session_Id}{'NAS-IP-Address'} = $NAS_IP_Address;
		if ( $Acct_Status_Type eq "Start" ) {
			$sessions{$Acct_Unique_Session_Id}{'Timestamp-Start'} = $Timestamp_Start;
		}
		else  {
			$sessions{$Acct_Unique_Session_Id}{'Timestamp-Stop'} = $Timestamp_Stop;
		}
		$sessions{$Acct_Unique_Session_Id}{'Acct-Session-Time'} = $Acct_Session_Time;
		$sessions{$Acct_Unique_Session_Id}{'Acct-Output-Octets'} = $Acct_Output_Octets;
		$sessions{$Acct_Unique_Session_Id}{'Acct-Input-Octets'} = $Acct_Input_Octets;
		$sessions{$Acct_Unique_Session_Id}{'Acct-Terminate-Cause'} = $Acct_Terminate_Cause;


		$cnt++;
	}

}


#print "CTN $cnt \n";

print "User,Anonymised_User,Router_IP,VPN_User_IP,VPN_Server_IP,TS_Start,TS_Stop,Session_Start,Duration,Output,Input,Cause,URLs", "\n";
foreach my $key ( keys %sessions ) {
	#print "$key: ";
	$ts=$sessions{$key}{'Timestamp-Start'};
	my ($sec, $min, $hour, $day,$month,$year) = (localtime($ts))[0,1,2,3,4,5]; 

	$formatted_date = sprintf("%02d/%02d/%d %02d:%02d:%02d", $day, $month + 1, $year + 1900, $hour, $min, $sec);
	$Anonymised_User_Name = md5_base64($sessions{$key}{'User-Name'});

	print $sessions{$key}{'User-Name'}, ",";
	print $Anonymised_User_Name, ",";
	print $sessions{$key}{'Calling-Station-Id'}, ",";
	print $sessions{$key}{'Framed-IP-Address'}, ",";
	print $sessions{$key}{'NAS-IP-Address'}, ",";
	print $sessions{$key}{'Timestamp-Start'}, ",";
	print $sessions{$key}{'Timestamp-Stop'}, ",";
	print $formatted_date, ",";
	print $sessions{$key}{'Acct-Session-Time'}, ",";
	print $sessions{$key}{'Acct-Output-Octets'}, ",";
	print $sessions{$key}{'Acct-Input-Octets'}, ",";
	print $sessions{$key}{'Acct-Terminate-Cause'}, ",";

	$URLs=`/usr/sbin/httpry -f 'method,host,request-uri' -r /home/tcpdump/tcpdump.ppp0_$ts 'dst port 80' 2>/dev/null`;
	$URLs =~ s/\n/\^/g;
	$URLs =~ s/GET\s+/http:\/\//g;
	$URLs =~ s/\s+\//http:\//g;
	print $URLs;
	print "\n";

	
}

#print Dumper %sessions;

