package WowWee::RoboPanda;

use strict;
use Exporter;
use vars qw($VERSION @ISA @EXPORT @EXPORT_OK %EXPORT_TAGS);
use Time::HiRes 'sleep';

use Data::Dumper;
use Device::Firmata::Constants ":all";
use Device::Firmata;
$|=1;



our $VERSION      = 1.00;
our @ISA          = qw(Exporter);
our @EXPORT       = ();
our @EXPORT_OK    = qw();
our %EXPORT_TAGS  = ();

my $ANALOG  = 'A';  #Analog input/output
my $DIGITAL = 'D';  #Digital input/output
my $PWMO    = 'PO'; #Digital output with optional PWM output (LEDs, etc...)
my $PWM     = 'P';  #PWM output (audio, ir, etc...)

sub new {
  #create a new RoboPanda object with specifed sensor values, or use default values if not specified
  my ($class, %args) = @_;
  my $self = bless ({},$class);

  $self->{'debug'}              = $args{'-debug'}                 || 0;
  print "WowWee::RoboPanda->new()...\n" if $self->{'debug'};

  $self->{'headlr_type'}        = $args{'-headlr_type'}           || $ANALOG;
  $self->{'headlr'}             = $args{'-headlr'}                || 850;
  $self->{'headlr_min'}         = $args{'-headlr_min'}            || 800;
  $self->{'headlr_max'}         = $args{'-headlr_max'}            || 900;
	#$self->{'headl_out'}          = $args{'-headl_out'}             || 22; #HEAD-L OUTPUT PIN
	#$self->{'headr_out'}          = $args{'-headl_out'}             || 24; #HEAD-R OUTPUT PIN
  #$self->{'headlr_in'}           = $args{'-headlr_in'}            || ; #HEAD-LR INPUT PIN
  
  $self->{'headud_type'}        = $args{'-headud_type'}           || $ANALOG;
  $self->{'headud'}             = $args{'-headud'}                || 850;
  $self->{'headud_min'}         = $args{'-headud_min'}            || 800;
  $self->{'headud_max'}         = $args{'-headud_max'}            || 900;
	#$self->{'headu_out'}          = $args{'-headu_out'}             || 26; #HEAD-U OUTPUT PIN
	#$self->{'headd_out'}          = $args{'-headd_out'}             || 28; #HEAD-D OUTPUT PIN
	#$self->{'headud_in'}           = $args{'-headud_in'}            || ; #HEAD-UD INPUT PIN
	
  $self->{'eyebrow_type'}       = $args{'-eyebrow_type'}          || $ANALOG;
  $self->{'eyebrow'}            = $args{'-eyebrow'}               || 850;
  $self->{'eyebrow_min'}        = $args{'-eyebrow_min'}           || 800;
  $self->{'eyebrow_max'}        = $args{'-eyebrow_max'}           || 900;
	#$self->{'eyebrowu_out'}       = $args{'-eyebrowu_out'}          || 30; #EYEU OUTPUT PIN
	#$self->{'eyebrowd_out'}       = $args{'-eyebrowd_out'}          || 32; #EYED OUTPUT PIN
	#$self->{'eyebrowu_in'}        = $args{'-eyebrowu_in'}           || ; #EYEU INPUT PIN (Limit Switch)
	#$self->{'eyebrowd_in'}        = $args{'-eyebrowd_in'}           || ; #EYED INPUT PIN (Limit Switch)
	

  $self->{'accelerometer_type'} = $args{'-accelerometer_type'}    || $ANALOG;
  $self->{'accelerometer_x'}    = 0;
  $self->{'accelerometer_y'}    = 0;
  $self->{'accelerometer_x_in'} = $args{'accelerometer_x_in'}     || 'A0'; #TILT_X INPUT PIN
  $self->{'accelerometer_y_in'} = $args{'accelerometer_y_in'}     || 'A1'; #TILT_Y INPUT PIN

  #$self->{'cart_sw_type'}      = $args{'-cart_sw_type'}          || $DIGITAL;
  #$self->{'cart_sw'}           = 0;
  #$self->{'cart_sw_in'}         = $args{'cart_sw_in'}             ||; #J15 INPUT PIN

  #$self->{'ball_sw_type'}      = $args{'-ball_sw_type'}          || $DIGITAL;
  #$self->{'ball_sw'}           = 0;
  #$self->{'ball_sw_in'}         = $args{'ball_sw_in'}             || ; #Ball Switch INPUT PIN

  $self->{'eye_left_led_type'}  = $args{'-eye_left_led'}          || $PWMO;
  $self->{'eye_left_led'}       = $args{'-eye_left_led'}          || 0;
  #$self->{'eye_left_led_out'}   = $args{'-eye_left_led_out'}      || ; #L-EYE-LED OUTPUT PIN
  
  $self->{'eye_right_led_type'} = $args{'-eye_right_led'}         || $PWMO;
  $self->{'eye_right_led'}      = $args{'-eye_right_led'}         || 0;
  #$self->{'eye_right_led_out'}  = $args{'-eye_right_led_out'}     || ; #R-EYE-LED OUTPUT PIN
    
  $self->{'chest_led_type'}     = $args{'-chest_led'}             || $PWMO;
  $self->{'chest_led'}          = $args{'-chest_led'}             || 0;
  #$self->{'chest_led_out'}      = $args{'-chest_led_out'}         || ; #CHEST-LED OUTPUT PIN

  $self->{'ir_trans_type'}      = $args{'-ir_trans_type'}         || $DIGITAL;
  $self->{'ir_trans'}           = 0;
  #$self->{'ir_trans_out'}       = $args{'ir_trans_out'}           || ; #IR_TX OUTPUT PIN
  
  $self->{'ir_receive_type'}    = $args{'-ir_receive_type'}       || $DIGITAL;
  $self->{'ir_receive'}         = 0;
  #$self->{'ir_receive_in'}      = $args{'ir_receive_in'}          || ; #IR_RX OUTPUT PIN

  $self->{'palm_left_led_type'} = $args{'-palm_left_led_type'}    || $PWMO;
  $self->{'palm_left_led'}      = $args{'-palm_left_led'}         || 0;
  #$self->{'palm_left_led_out'}  = $args{'-palm_left_led_out'}     || ; #L-PALM-LED OUTPUT PIN

  $self->{'palm_right_led_type'}= $args{'-palm_right_led_type'}   || $PWMO;
  $self->{'palm_right_led'}     = $args{'-palm_right_led'}        || 0;
  #$self->{'palm_right_led_out'} = $args{'-palm_right_led_out'}    || ; #R-PALM-LED OUTPUT PIN

  $self->{'earfb_type'}         = $args{'-earfb_type'}            || $ANALOG;
  $self->{'earfb'}              = $args{'-earfb'}                 || 0;
  $self->{'earfb_min'}          = $args{'-earfb_min'}             || 0;
  $self->{'earfb_max'}          = $args{'-earfb_max'}             || 0;
  #$self->{'earf_out'}           = $args{'-earf_out'}              || ; #EAR-F OUTPUT PIN
  #$self->{'earb_out'}           = $args{'-earb_out'}              || ; #EAR-B OUTPUT PIN
  #$self->{'earu_in'}            = $args{'-earu_in'}               || ; #EARU INPUT PIN
  #$self->{'eard_in'}            = $args{'-eard_in'}               || ; #EARD INPUT PIN
  
  $self->{'leg_rightfb_type'}   = $args{'-leg_rightfb_type'}      || $ANALOG;
  $self->{'leg_rightfb'}        = $args{'-leg_rightfb'}           || 0;
  $self->{'leg_rightfb_min'}    = $args{'-leg_rightfb_min'}       || 0;
  $self->{'leg_rightfb_max'}    = $args{'-leg_rightfb_max'}       || 0;
  #$self->{'leg_rightf_out'}     = $args{'-leg_rightf_out'}        || ; #R-LEG-F OUTPUT PIN
  #$self->{'leg_rightb_out'}     = $args{'-leg_rightb_out'}        || ; #R-LEG-B OUTPUT PIN
  #$self->{'leg_rightfb_in'}      = $args{'-leg_rightfb_in'}       || ; #R-LEG-FB INPUT PIN

  $self->{'leg_leftfb_type'}    = $args{'-leg_leftfb_type'}       || $ANALOG;
  $self->{'leg_leftfb'}         = $args{'-leg_leftfb'}            || 0;
  $self->{'leg_leftfb_min'}     = $args{'-leg_leftfb_min'}        || 0;
  $self->{'leg_leftfb_max'}     = $args{'-leg_leftfb_max'}        || 0;
  #$self->{'leg_leftf_out'}      = $args{'-leg_leftf_out'}         || ; #L-LEG-F OUTPUT PIN
  #$self->{'leg_leftb_out'}      = $args{'-leg_leftb_out'}         || ; #L-LEG-B OUTPUT PIN
  #$self->{'leg_leftfb_in'}      = $args{'-leg_leftfb_in'}         || ; #L-LEG-FB INPUT PIN

  $self->{'arm_leftoc_type'}    = $args{'-arm_leftoc_type'}       || $ANALOG;
  $self->{'arm_leftoc'}         = $args{'-arm_leftoc'}            || 0;
  $self->{'arm_leftoc_min'}     = $args{'-arm_leftoc_min'}        || 0;
  $self->{'arm_leftoc_max'}     = $args{'-arm_leftoc_max'}        || 0;
  #$self->{'arm_lefto_out'}      = $args{'-arm_lefto_out'}         || ; #L-ARM-O OUTPUT PIN
  #$self->{'arm_leftc_out'}      = $args{'-arm_leftc_out'}         || ; #L-ARM-C OUTPUT PIN
  #$self->{'arm_leftoc_in'}      = $args{'-arm_leftoc_in'}         || ; #L-ARM-OC INPUT PIN

	$self->{'hand_leftud_type'}   = $args{'-hand_leftud_type'}      || $ANALOG;
  $self->{'hand_leftud'}        = $args{'-hand_leftud'}           || 0;
  $self->{'hand_leftud_min'}    = $args{'-hand_leftud_min'}       || 0;
  $self->{'hand_leftud_max'}    = $args{'-hand_leftud_max'}       || 0;
  #$self->{'hand_leftu_out'}     = $args{'-hand_leftu_out'}        || ; #L-HAND-U OUTPUT PIN
  #$self->{'hand_leftd_out'}     = $args{'-hand_leftd_out'}        || ; #L-HAND-D OUTPUT PIN
	#$self->{'hand_leftud_in'}     = $args{'-hand_leftud_in'}        || ; #L-HAND-UD INPUT PIN

  $self->{'arm_rightoc_type'}   = $args{'-arm_rightoc_type'}      || $ANALOG;
  $self->{'arm_rightoc'}        = $args{'-arm_rightoc'}           || 0;
  $self->{'arm_rightoc_min'}    = $args{'-arm_rightoc_min'}       || 0;
  $self->{'arm_rightoc_max'}    = $args{'-arm_rightoc_max'}       || 0;
  #$self->{'arm_righto_out'}     = $args{'-arm_righto_out'}       || ; #R-ARM-O OUTPUT PIN
  #$self->{'arm_rightc_out'}     = $args{'-arm_rightc_out'}       || ; #R-ARM-C OUTPUT PIN
  #$self->{'arm_rightoc_in'}      = $args{'-arm_rightoc_in'}         || ; #R-ARM-OC INPUT PIN

  $self->{'hand_rightud_type'}  = $args{'-hand_rightud_type'}     || $ANALOG;
  $self->{'hand_rightud'}       = $args{'-hand_rightud'}          || 0;
  $self->{'hand_rightud_min'}   = $args{'-hand_rightud_min'}      || 0;
  $self->{'hand_rightud_max'}   = $args{'-hand_rightud_max'}      || 0;
  #$self->{'hand_rightu_out'}    = $args{'-hand_rightu_out'}       || ; #R-HAND-U OUTPUT PIN
  #$self->{'hand_rightd_out'}    = $args{'-hand_rightd_out'}       || ; #R-HAND-D OUTPUT PIN
  #$self->{'hand_rightud_in'}    = $args{'-hand_rightoc_in'}       || ; #R-HAND-OC INPUT PIN

  $self->{'serial_port'}        = $args{'-serial_port'}           || undef;
 
  #if ($self->{'debug'}){
  # #display default sensor values
  # print "\tinitialization variables...\n";
  # foreach my $element (sort keys %{$self}){
  #   print "\t$element - " . $self->{$element} . "\n";
  # }
  #}
  
  print "\tInitializing serial port communication\n" if $self->{'debug'};
  if ($self->{'serial_port'}){ #exit with an error if a serial port is not defined
  #  $self->{'serial'} = Device::Firmata->open( $self->{'serial_port'} ) || die "Could not connect to Firmata serial port\n";
  #  if ( $self->{'debug'} ){
  #  	foreach my $key ( keys(%{$self->{'serial'}}) ){
  #  		print "\t\t$key\n";
  #  	}
  #	}
  } else {
    die "ERROR: Serial port not specified\n";
  }
  print "init>\n" if $self->{'debug'};
  init_sensors($self);  #initialize all output sensors to their default values
  print "<init\n" if $self->{'debug'};
  return $self;
}

sub init_sensors {
  #write default values to all output sensors
  my ($self, undef) = @_;
  print "\tWowWee::RoboPanda->init_sensors()...\n" if $self->{'debug'};
  foreach my $sensor (sort keys %{$self}){
    next unless ($sensor =~ s/_type//);
    print "$sensor\n" if $self->{'debug'};
    my $sensorType = $self->{$sensor . "_type"};
    if ($sensorType eq 'A'){
      $self->writeAnalog($sensor, $self->{$sensor});
    } else {
      $self->writeDigital($sensor,$self->{$sensor});
    }
  }
  $self->updateState('all');
}

sub updateState {
  #read all analog and digital sensors and update state variables with current values
  my ($self, $sensor) = @_;
  print "WowWee::RoboPanda->updateState($sensor)...\n" if $self->{'debug'};
  if ($sensor eq 'all'){
    foreach my $stateVar (sort keys %{$self}){
      next unless ($stateVar =~ s/_type//);
      my $sensorType = $self->{$stateVar . "_type"};
      if ($sensorType eq 'A'){
        $self->{$stateVar} eq $self->readAnalog($stateVar);
      } else {
        $self->{$stateVar} eq $self->readDigital($stateVar);
      }
    }
  } else {
    my $sensorType = $self->{$sensor . "_type"};
    if ($sensorType eq 'A'){
      $self->{$sensor} eq $self->readAnalog($sensor);
    } else {
      $self->{$sensor} eq $self->readDigital($sensor);
    }
  }
}

sub readAnalog {
  #read Analog sensor value and assign results to $self->{$sensor}
  my ($self, $sensor) = @_;
  print "\tWowWee::RoboPanda->readAnalog($sensor)...\n" if $self->{'debug'};
  return $self->{$sensor};
}

sub readDigital {
  #read Digital sensor and assign results to $self->{$sensor}
  my ($self, $sensor) = @_;
  print "\tWowWee::RoboPanda->readDigital($sensor)...\n" if $self->{'debug'};
  return undef;
}

sub writeAnalog {
  #write Analog sensor value
  my ($self, $sensor, $value) = @_;
  print "\tWowWee::RoboPanda->writeAnalog($sensor, $value)...\n" if $self->{'debug'};
  return undef;
}

sub writeDigital {
  #write Digital sensor value
  my ($self, $sensor, $value) = @_;
  print "\tWowWee::RoboPanda->writeDigital($sensor, $value)...\n" if $self->{'debug'};
  return undef;
}

sub headlr {
  #$reqPos = percent of range to move (1-100)
  my ($self, $reqPos) = @_;
  print "\tWowWee::RoboPanda->headlr($reqPos)...\n" if $self->{'debug'};
  if ( $reqPos > 100 || $reqPos < 1){
    print "\trequested position ($reqPos) is not an acceptable percentage 1-100" if $self->{'debug'};
    return(1);
  }
  print "\trequested position=$reqPos\n" if $self->{'debug'};
  print "\theadlr_min=" . $self->{'headlr_min'} . "\n" if $self->{'debug'};
  print "\theadlr_max=" . $self->{'headlr_max'} . "\n" if $self->{'debug'};
  $reqPos = ($self->{'headlr_min'} + ( ($self->{'headlr_max'} - $self->{'headlr_min'}) * ($reqPos/100) )) . "\n" if $self->{'debug'};
  print "\t\$reqPos=$reqPos\n" if $self->{'debug'};

  $self->updateState('headlr');

  return if $self->checkReqPos('headlr', $reqPos);#is $reqPos within mix/max range

  #move headlr to $reqPos
  if ( $self->{'headlr'} < $reqPos ){
    #increment position
    $self->writeDigital('headl', 1);
  } elsif ( $self->{'headlr'} > $reqPos ) {
    #decrement position
    $self->writeDigital('headr', 1);
  }
  print "\tdelaying " . $self->{'headlr_delay'} . " milliseconds\n" if $self->{'debug'};
  Time::HiRes::usleep $self->{'headlr_delay'};
  $self->writeDigital('headl', 0);
  $self->writeDigital('headr', 0);
  return $self->{'headlr'};
}

sub headud {
  #$reqPos = percent of range to move (1-100)
  my ($self, $reqPos) = @_;
  print "\tWowWee::RoboPanda->headud($reqPos)...\n" if $self->{'debug'};
  $reqPos /= 100;
  print "\t\$reqPos=$reqPos\n" if $self->{'debug'};
  print "\theadud_min=" . $self->{'headud_min'} . "\n" if $self->{'debug'};
  print "\theadud_max=" . $self->{'headud_max'} . "\n" if $self->{'debug'};
  print "\t\$reqPos=" . ($self->{'headud_min'} + ( ($self->{'headud_max'} - $self->{'headud_min'}) * $reqPos )) . "\n" if $self->{'debug'};
  #
  #move headlr to $reqPos
  #
  $self->updateState('headud');
  return $self->{'headud'};
}

sub checkReqPos{
  #test if requested position is within the minimum and maximum range
  my ($self, $sensor, $reqPos) = @_;
  print "\tWowWee::RoboPanda->checkReqPos($sensor)\n" if $self->{'debug'};
  if ($self->{$sensor . "_min"}){
    if ($reqPos < ($self->{$sensor . "_min"})) {
      print "requested position $reqPos is less than $sensor" . "_min (" . $self->{$sensor . "_min"} . ")\n" if $self->{'debug'};
      return(1);
    } elsif ($reqPos > ($self->{$sensor . "_max"})){
      print "requested position $reqPos is greater than $sensor" . "_max (" . $self->{$sensor . "_max"} . ")\n" if $self->{'debug'};
      return(1);
    }
  }
  return(0);
}

1;