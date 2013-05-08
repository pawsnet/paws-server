#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use strict;

print header;
print start_html(
	-title	=>	'PAWS Password Change',
	-style	=>	{'src'	=>	'/styles/style.css'},
);
print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 

my $dbh = DBI->connect( "dbi:mysql:radius", "radius", "radius_Par0la") or 	
    &dienice("Can't connect to db: $DBI::errstr");
	
my $username = param('username');
my $oldpass = param('oldpass');
my $newpass1 = param('newpass1');
my $newpass2 = param('newpass2');


if (! defined $username ) {
	&print_form;
	exit(0)
}

if ($username !~ /^\w{3,10}$/) {
	&dienice("Please use an alphanumeric username between 3 and 10 letters long, with no spaces.");   
}

if ($newpass1 !~ /^\w{8,24}$/) {
	&dienice("Please use an alphanumeric value for new password  between 8 and 24 letters long, with no spaces.");   
}
if ($newpass2 !~ /^\w{8,24}$/) {
	&dienice("Please use an alphanumeric value for new password confirmation  between 8 and 24 letters long, with no spaces.");   
}

if ($newpass1 ne $newpass2) {
   &dienice("You didn't type the same thing for both new password fields. Please check it and try again.");
}


my $rec;
my $sth = $dbh->prepare("select * from radcheck where username = ? and value = ?") or &dbdie;
$sth->execute($username, $oldpass) or &dbdie;
unless ( $rec = $sth->fetchrow_hashref) {
	#print "DU: $rec->{username}, DP: $rec->{value}\n";
    &dienice("Username or password incorrect in PAWS database!");
}

#my $rec = $sth->fetchrow_hashref; 

#my $uinfo = $sth->fetchrow_hashref;

#if (! defined $rec ) {
#	print "NOT DEFINEd\n";
#}


#if ($rec->{value} ne $oldpass) {
#   &dienice(qq(Your old password is incorrect. If you can't remember it, please use the <a href="../forgotpass.html">reset password</a> form instead.));
#}

# now store it in the database...
$sth = $dbh->prepare("update radcheck  set value=? where username=?") or &dbdie; 
$sth->execute($newpass1, $username) or &dbdie;

print qq(<h2>Success!</h2>
<p>Your password has been changed! </p>\n);
print end_html;
exit 0;

###############################################

sub print_form {


	print qq(<h1>Change your PAWS password:</h1>);
	print start_form;

	print table(
	Tr(
		td('Username:'),
		td(
			textfield(
				-name 	=>	'username',
				-size	=>	'16',
				-maxlength	=>	'16',
				)
		)
	),

	Tr(
		td('Old password:'),
		td(
			password_field(
				-name 	=>	'oldpass',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	Tr(
		td('New password:'),
		td(
			 password_field(
				-name 	=>	'newpass1',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	Tr(
		td('New password again:'),
		td(
			password_field(
				-name 	=>	'newpass2',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	);




	print submit(
		-name	=>	'submit_form',
		-value	=>	'Change Password',
	);

	print end_form;
	print end_html;
}


sub dienice {
    my($msg) = @_;
    #print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 
    print "<h2>Error</h2>\n";
    print $msg;
    exit;
}

sub dbdie {
    my($package, $filename, $line) = caller;
    my($errmsg) = "Database error: $DBI::errstr<br>
                called from $package $filename line $line";
    &dienice($errmsg);
}



