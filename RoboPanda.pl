use warnings;
use strict;
use WowWee::RoboPanda;

my $SerialPort = 'COM14';

my $robopanda = WowWee::RoboPanda->new(
    -debug          => 1,
    -serial_port    => $SerialPort,
  );

#$robopanda->headlr(1); #move headlr to 1% (far left)
#$robopanda->headlr(100); #move headlr to 100% (far right)
