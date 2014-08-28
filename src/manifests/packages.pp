class src::packages inherits src::params {
  Package {
    allow_virtual => false,
  }
  
  package { $rpms:
    ensure => latest
  }
  
  package { $pips:
    ensure   => latest,
    provider => pip,
    require  => Package[$pip_deps],
  }
  
  package { $gems:
    ensure   => latest,
    provider => gem,
    require  => Package['rubygems'],
  }
}
