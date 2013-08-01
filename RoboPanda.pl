#!/usr/bin/perl
use warnings;
use strict;
use WowWee::RoboPanda;

my $COMPORT = 'COM12';

my $robopanda = WowWee::RoboPanda->new(
  	-debug 				=> 1,
		-serial_port	=> 'COM12',
	);

#$robopanda->headlr(1); #move headlr to 1% (far left)
#$robopanda->headlr(100); #move headlr to 100% (far right)
