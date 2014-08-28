class src {
  class { 'src::packages': }
  -> class { 'src::services': }
}
