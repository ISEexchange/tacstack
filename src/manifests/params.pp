class src::params {
  $gems = [
    'etcd',
    'sass',
  ]
  
  $pips = [
    'MySQL-python',
    'lxml',
    'robotframework',
    'supervisor',
    'python-etcd'
  ]
  
  # These RPMs must be installed before pips.
  $pip_deps = [
    'mysql',
    'python-pip',
    'python-setuptools',
  ]
  
  $rpms = [
    'autoconf',
    'automake',
    'bash-completion',
    'bison',
    'byacc',
    'cscope',
    'ctags',
    'diffstat',
    'doxygen',
    'flex',
    'gcc',
    'gcc-c++',
    'httpd',
    'indent',
    'intltool',
    'libtool',
    'libxml2',
    'libxml2-devel',
    'libxml2-python',
    'libxslt',
    'libxslt-devel',
    'libxslt-python',
    'mysql',
    'mysql-devel',
    'mysql-server',
    'openssh-clients',
    'openssh-server',
    'passwd',
    'patchutils',
    'php',
    'php-devel',
    'php-gd',
    'php-mysql',
    'php-pecl-memcache',
    'php-pspell',
    'php-snmp',
    'php-xml',
    'php-xmlrpc',
    'python',
    'python-devel',
    'python-lxml',
    'python-nose',
    'python-pep8',
    'python-pip',
    'python-setuptools',
    'ruby',
    'rubygems',
    'subversion',
    'swig',
    'unzip',
    'vim-enhanced',
  ]
}
