package WowWee::RoboPanda_Serial;
use strict;use Exporter;use vars qw($VERSION @ISA @EXPORT @EXPORT_OK %EXPORT_TAGS);our $VERSION = 1.00; our @ISA = qw(Exporter); our (@EXPORT,@EXPORT_OK,%EXPORT_TAGS);

sub new{
  my (%args) = @_;
  my $self;
  $self->{'debug'}		= $args{'-debug'}        || 0;
  $self->{'serial_port'}			= $args{'-port'}         || undef;
  $self->{'serial_quiet'}		= $args{'-quiet'}        || undef;
  $self->{'serial_databits'}	= $args{'-databits'}     || 8;
  $self->{'serial_baudrate'}	= $args{'-baudrate'}     || 9600;
  $self->{'serial_stopbits'}	= $args{'-stopbits'}     || 1;
  $self->{'serial_parity'}		= $args{'-parity'}     	 || "none";
  print "\tWowWee::RoboPanda::serial()...\n" if $self->{'debug'};
  unless ($self->{'serial_port'}){
  	print "\tserial port not specified...\n";
  	return(1);
  }                                     

	if ($^O =~ /win/i){
		use Win32::SerialPort qw( :STAT 0.19 );
		$self->{'serial'} = new Win32::SerialPort($self->{'serial_port'}, 1);
	} else {
		require Device::SerialPort;
		$self->{'serial'} = new Device::SerialPort($self->{'serial_port'}, 1);
	}

	if ($self->{'serial'}){
		if ($self->{'serial'}->baudrate eq $self->{'serial_baud'}){
		} else {
			#
			### TODO: support return of multiple baudrates from $self->{'serial'}->baudrate
			#			
			print "\trequested baud (" . $self->{'serial_baud'} . ") is not available.  Using " . $self->{'serial'}->baudrate . "\n";
			$self->{'serial_baud'} = $self->{'serial'}->baudrate;
		}
		$self->{'serial'}->baudrate( $self->{'serial_baud'} );
		$self->{'serial'}->databits( $self->{'serial_databits'} );
		$self->{'serial'}->parity( $self->{'serial_parity'} );
		$self->{'serial'}->stopbits( $self->{'serial_stopbits'} );
		$self->{'serial'}->write_settings || return(1);
		print "\tattached serial port...\n" if ($self->{'debug'} && $self->{'serial'});
	} else {
		print "\tCan't change Device_Control_Block: $^E\n";
		return(1);
	}
	print "\tserial: " . $self->{'serial'}->user_msg() . "\n";
	return ($self->{'serial'});
}

1;