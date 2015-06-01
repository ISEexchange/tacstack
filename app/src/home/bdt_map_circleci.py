import os
import sys
import git
import errno
import MySQLdb
import fileinput
import xmlrpclib
import subprocess


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def set_file_perms(f_name, perm):
    try:
        os.chmod(f_name, perm)
    except Exception, e:
        print 'Failed to chmod %s to %s' % (f_name, perm)
        print 'Exception: %s' % e
        return False
    print '\nChanged permissions for %s to %s' % (f_name, str(perm))


def import_map_db():
    db_file = '/home/bdt/map/src/map_database/map_db_ref_data.sql'
    print '\nImporting map_db database from %s' % db_file
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='')
    cursor = conn.cursor()
    try:
        cursor.execute('\n'.join(open(db_file).readlines()))
    except Exception, e:
        print 'Failed to import map_db from %s' % db_file
        print 'Exception: %s' % e
        return False


def create_symlinks():
    root_dir = '/home/bdt/map/src/map_frontend_web_gui/'
    dest_dir = '/var/www/localhost/htdocs/map'
    print '\nCreating symlinks for %s -> %s' % (dest_dir, root_dir)
    for dir_name, subdir_list, files in os.walk(root_dir):
        for f_name in files:
            src_path = os.path.join(dir_name, f_name)
            dst_path = os.path.join(dest_dir, dir_name.split(root_dir)[1])
            make_sure_path_exists(dst_path)
            full_dst_path = os.path.join(dst_path, f_name)
            try:
                os.symlink(src_path, full_dst_path)
            except Exception, e:
                print 'Failed to create symlink',
                print "'%s' -> '%s'" % (full_dst_path, src_path)
                print 'Exception: %s' % e
                return False

    root_dir = '/var/ftp/pub/uploads'
    dest_dir = '/var/www/localhost/htdocs/map/results'
    print 'Creating symlinks for %s -> %s' % (dest_dir, root_dir)
    try:
        os.symlink(root_dir, dest_dir)
    except Exception, e:
        print 'Failed to create symlink',
        print "'%s' -> '%s'" % (full_dst_path, src_path)
        print 'Exception: %s' % e
        return False
    print 'Successfully created symlinks'

    root_dir = '/var/ftp/pub/uploads/reports/'
    dest_dir = '/var/www/localhost/htdocs/map/reports'
    print 'Creating symlinks for %s -> %s' % (dest_dir, root_dir)
    try:
        os.symlink(root_dir, dest_dir)
    except Exception, e:
        print 'Failed to create symlink',
        print "'%s' -> '%s'" % (full_dst_path, src_path)
        print 'Exception: %s' % e
        return False
    print 'Successfully created symlinks'


def update_httpd_settings():
    print '\nSetting httpd DocumentRoot to /var/www/localhost/htdocs/map'
    set_file_perms('/etc/phpmyadmin/config.inc.php', 0644)
    for line in fileinput.input('/etc/apache2/httpd.conf', inplace=True):
        print line.replace(
            'DocumentRoot "/var/www/localhost/htdocs"',
            'DocumentRoot "/var/www/localhost/htdocs/map"'),


def process_control():
    server_url = 'http://localhost:9001/RPC2'
    try:
        server = xmlrpclib.Server(server_url)
    except Exception, e:
        print 'Failed to connect to %s' % server_url
        print 'Exception: %s' % e
        return False
    print '\nRestarting httpd with supervisor'
    try:
        server.supervisor.stopProcess('httpd')
    except Exception, e:
        print 'Failed to stop httpd'
        print 'Exception: %s' % e
        return False
    try:
        server.supervisor.startProcess('httpd')
    except Exception, e:
        print 'Failed to start httpd'
        print 'Exception: %s' % e
        return False
    print 'Starting map with supervisor'
    try:
        server.supervisor.startProcess('map')
    except Exception, e:
        print 'Failed to start map'
        print 'Exception: %s' % e
        return False


if __name__ == "__main__":

    user   = sys.argv[1]
    token  = sys.argv[2]
    branch = sys.argv[4]

    # Download the repos
    os.chdir('/home')
    repo = 'https://%s:%s@github.com/ISEexchange/robotframework.git' % (user, token)
    subprocess.Popen('git clone %s' % repo, shell=True, stdout=subprocess.PIPE).communicate()

    repo = "https://%s:%s@github.com/ISEexchange/bdt.git" % (user, token)
    subprocess.Popen('git clone %s' % repo, shell=True, stdout=subprocess.PIPE).communicate()

    # Check out the branch this pull request is for
    os.chdir('/home/bdt')
    subprocess.Popen('git fetch origin %s/head:test_branch ' % (branch), shell=True, stdout=subprocess.PIPE).communicate()
    subprocess.Popen('git checkout test_branch', shell=True, stdout=subprocess.PIPE).communicate()

    os.chdir('/home')

    # Import map_db
    import_map_db()

    # Create front end symbolic links
    create_symlinks()

    # Update httpd settings
    update_httpd_settings()

    # Restart/start supervisor processes
    process_control()

    print "\nYou're all set!\n"

