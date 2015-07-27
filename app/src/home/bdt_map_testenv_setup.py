import os
import sys
import git
import errno
import MySQLdb
import fileinput
import xmlrpclib
import subprocess


ISE_REPOS = {
    'bdt': 'git@github.com:ISEexchange/bdt.git',
    'robotframework': 'git@github.com:ISEexchange/robotframework.git'
}


def ask_for_key_import():
    print 'Would you like to import your SSH keys for Github communication? y|n'
    line = sys.stdin.readline()
    if line.rstrip('\n') == 'y':
        return True
    else:
        return False


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
        print 'Failed to chmod %s to %s' % (f_name, oct(perm))
        print 'Exception: %s' % e
        return False
    print '\nChanged permissions for %s to %s' % (f_name, oct( perm))


def get_multiline_input(breaker):
    captured = ''
    while True:
        line = sys.stdin.readline()
        if breaker in line:
            captured += line.rstrip('\n')
            break
        else:
            captured += line
    return captured


def get_keys():
    print "\nLet's import your ssh keys to make talking to Github easier"
    print "Enter private key for ssh'ing to Github"
    private_key = get_multiline_input('END RSA PRIVATE KEY')
    print 'Successfully captured private key'
    print '\nEnter matching public key'
    public_key = sys.stdin.readline()
    print 'Successfully captured public key'
    return {'pri': private_key, 'pub': public_key}


def store_keys(keys):
    pri_file = '/root/.ssh/id_rsa'
    print '\nWriting private key to %s' % pri_file
    try:
        f = open(pri_file, 'w')
        f.write(keys['pri'])
        f.close()
    except Exception, e:
        print 'Failed to open and/or write to %s' % pri_file
        print 'Exception: %s' % e
        return False
    set_file_perms(pri_file, 0600)
    print 'Saved private key into %s. Set permission to %s' % (pri_file, '0600')

    pub_file = '/root/.ssh/id_rsa.pub'
    print '\nWriting public key to %s' % pub_file
    try:
        f = open(pub_file, 'w')
        f.write(keys['pub'])
        f.close()
    except Exception, e:
        print 'Failed to open and/or write to %s' % pub_file
        print 'Exception: %s' % e
        return False
    set_file_perms(pub_file, 0644)
    print 'Saved public key into %s. Set permission to %s' % (pub_file, '0644')


def clone_repo(name, conn_type):
    print "\nWhats the %s clone URL for your forked %s repo?" % (
        conn_type, name)
    user_repo = sys.stdin.readline().rstrip('\n')
    try:
        repo = git.Repo.clone_from(user_repo, name)
    except Exception, e:
        print "Failed to clone repo: '%s'" % user_repo
        print 'Exception: %s' % e
        return False
    dest_dir = os.path.join(os.getcwd(), name)
    print 'Successfully cloned %s into %s' % (user_repo, dest_dir)
    repo.create_remote('upstream', ISE_REPOS[name])
    print 'Successfully added upstream repo %s' % ISE_REPOS[name]


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

    print 'Starting nodejs with supervisor'
    try:
        server.supervisor.startProcess('nodejs')
    except Exception, e:
        print 'Failed to start nodejs'
        print 'Exception: %s' % e
        return False



if __name__ == "__main__":

    conn_type = 'HTTPS'
    # 0. Ask if they want to provide keys
    import_keys = ask_for_key_import()

    # 1. Get and save keys
    if import_keys:
        conn_type = 'SSH'
        store_keys(get_keys())
        # 2. Set correct permissions for config file
        set_file_perms('/root/.ssh/config', 0600)

    # 2. Get git config info
    print '\nWhat email address should we use for your git config?'
    cfg_email = sys.stdin.readline().rstrip('\n')
    subprocess.Popen(['git config --global user.email "%s"' % cfg_email], shell=True,
        stdout=subprocess.PIPE).communicate()
    print '\nWhat full name should we use for your git config?'
    cfg_name = sys.stdin.readline().rstrip('\n')
    subprocess.Popen(['git config --global user.name "%s"' % cfg_name], shell=True,
        stdout=subprocess.PIPE).communicate()

    # 3. Download the repos
    os.chdir('/home')
    clone_repo('bdt', conn_type)

    # 3a. Pull and go into develop branch
    print '\nWould you like to git pull upstream\'s develop branch? y|n'
    line = sys.stdin.readline()
    if line.rstrip('\n') == 'y':
        os.chdir('/home/bdt')
        r = subprocess.Popen(['git checkout -b develop'], shell=True,
            stdout=subprocess.PIPE).communicate()
        print r[0]
        print r[1]
        r = subprocess.Popen(['git pull --commit --no-edit upstream develop'], shell=True,
            stdout=subprocess.PIPE).communicate()
        print r[0]
        print r[1]

    # 3b. Install npm packages
    print '\nWould you like to install NodeJS\' npm packages? y|n'
    line = sys.stdin.readline()
    if line.rstrip('\n') == 'y':
        os.chdir('/home/bdt/map/src/map_nodejs_server')
        r = subprocess.Popen(['npm install'], shell=True,
            stdout=subprocess.PIPE).communicate()
        print r[0]
        print r[1]

    os.chdir('/home')
    clone_repo('robotframework', conn_type)

    os.chdir('/home')
    print '\nCloning glowing-configurator repo...'
    subprocess.Popen(['git clone git@github.com:cbautista1002/glowing-configurator.git'], shell=True,
            stdout=subprocess.PIPE).communicate()
    subprocess.Popen(['echo "source /home/glowing-configurator/.bashrc" >> ~/.bashrc'], shell=True,
            stdout=subprocess.PIPE).communicate()
    print "\nRun 'source  ~/.bashrc' to load new aliases from glowing-configurator"

    # 4. Import map_db
    import_map_db()

    # 5. Create front end symbolic links
    create_symlinks()

    # 6. Update httpd settings
    update_httpd_settings()

    # 7. Restart/start supervisor processes
    process_control()

    print "\nYou're all set!\n"

