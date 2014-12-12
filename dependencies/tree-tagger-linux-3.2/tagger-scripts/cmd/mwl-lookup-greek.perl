#!/usr/bin/perl

$month{"����������"} = 1;
$month{"�����������"} = 1;
$month{"�������"} = 1;
$month{"��������"} = 1;
$month{"�����"} = 1;
$month{"�����"} = 1;
$month{"�����"} = 1;
$month{"�������"} = 1;
$month{"�������"} = 1;
$month{"���������"} = 1;
$month{"�����������"} = 1;
$month{"���������"} = 1;
$month{"���������"} = 1;
$month{"����������"} = 1;

$month{"���������"} = 1;
$month{"����������"} = 1;
$month{"������"} = 1;
$month{"�������"} = 1;
$month{"����"} = 1;
$month{"������"} = 1;
$month{"������"} = 1;
$month{"��������"} = 1;
$month{"��������"} = 1;
$month{"����������"} = 1;
$month{"��������"} = 1;
$month{"��������"} = 1;
$month{"���������"} = 1;

while (<>) {
    chomp;
    if ($_ eq '') {
	print_sentence();
    }
    else {
	push @token, $_;
    }
}
print_sentence();

sub print_sentence {
    for( $i=0; $i<=$#token; $i++ ) {
	if (exists $month{$token[$i]}) {
	    $start = $end = $i;
	    if ($token[$start-1] =~ /^[1-9][0-9]?([���]�?)?(-[1-9][0-9]?([���]�?)?)?$/){
		$start--;
	    }
	    if ($token[$start-1] eq '������') {
		$start--;
	    }
	    if ($token[$end+1] eq '���') {
		$end++;
	    }
	    if ($token[$end+1] =~ /^(1[0-9][0-9][0-9]|20[0-9][0-9]|'[0-9][0-9])$/) {
		$end++;
	    }
	    for( $k=$start; $k<$end; $k++) {
		$join[$k] = 1;
	    }
	}
	elsif (($token[$i] eq "��'" && $token[$i+1] eq '���') ||
	       ($token[$i] eq '��' && 
		($token[$i+1] eq '����' || $token[$i+1] eq '����')))
	{
	    $join[$i] = 1;
	}
	       
    }
    for( $i=0; $i<=$#token; $i++ ) {
	if ($join[$i] == 1) {
	    print "$token[$i] "
	}
	else {
	    print "$token[$i]\n"
	}
    }
    undef @token;
    undef @join;
}
