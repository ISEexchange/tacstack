class src::services {
  Exec {
    path => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  }

  # Start mysqld to create initial tables.
  service { 'mysqld':
    ensure  => true,
    require => Package['mysql-server'],
  }
  
  exec { 'disable pam in sshd':
    command => 'sed -ri "s/UsePAM yes/UsePAM no/g" /etc/ssh/sshd_config',
    require => Package['openssh-server'],
    before  => Service['sshd'],
  }
  
  exec { 'set root password':
    command => 'echo root:changeme | chpasswd'
  }
  
  # Start sshd to create host keys.
  service { 'sshd':
    ensure  => true,
    require => Package['openssh-server'],
  }
  
  file { '/etc/supervisord.conf':
    ensure  => file,
    source  => 'puppet:///modules/src/supervisord.conf',
    require => Package['supervisor'],
  }

  file { '/var/www/html/phpinfo.php':
    ensure  => file,
    source  => 'puppet:///modules/src/phpinfo.php',
    require => Package['httpd'],
  }
}
