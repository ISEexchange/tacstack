import os
import sys
import git # pip install gitpython
import errno
import MySQLdb
import fileinput
import xmlrpclib


ISE_REPOS = {
    'bdt': 'git@github.com:ISEexchange/bdt.git',
    'robotframework': 'git@github.com:ISEexchange/robotframework.git'
}


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


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
    return {'pri':private_key, 'pub':public_key}


def store_keys(keys):
    pri_file = '/root/.ssh/id_rsa'
    print '\nWriting private key to %s' % pri_file
    f = open(pri_file, 'w')
    f.write(keys['pri'])
    f.close()
    os.chmod(pri_file, 0600)
    print 'Saved private key into %s. Set permission to %s' % (pri_file, '0600')

    pub_file = '/root/.ssh/id_rsa.pub'
    print '\nWriting public key to %s' % pub_file
    f = open(pub_file, 'w')
    f.write(keys['pub'])
    f.close()
    os.chmod(pub_file, 0644)
    print 'Saved public key into %s. Set permission to %s' % (pub_file, '0644')


def set_config_perms():
    cfg_file = '/root/.ssh/config'
    os.chmod(cfg_file, 0600)
    print '\nChanged permissions for %s to %s' % (cfg_file, '0600')

def clone_repo(name):
    print "\nWhats the SSH clone URL for your forked %s repo?" % name
    user_repo = sys.stdin.readline().rstrip('\n')
    repo = git.Repo.clone_from(user_repo, name)
    dest_dir = os.path.join(os.getcwd(), name)
    print 'Successfully cloned %s into %s' % (user_repo, dest_dir)
    repo.create_remote('upstream', ISE_REPOS[name])
    print 'Successfully added upstream repo %s' % ISE_REPOS[name]


def import_map_db():
    # db_file = '/home/bdt/map/map_db_ref_data.sql'
    db_file = '/home/m.sql'
    print '\nImporting map_db database from %s' % db_file
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='')
    cursor = conn.cursor()
    cursor.execute('\n'.join(open(db_file).readlines()))


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
            os.symlink(src_path, full_dst_path)

    root_dir = '/var/ftp/pub/uploads'
    dest_dir = '/var/www/localhost/htdocs/map/results'
    print 'Creating symlinks for %s -> %s' % (dest_dir, root_dir)
    os.symlink(root_dir, dest_dir)
    print 'Successfully created symlinks'

    root_dir = '/var/ftp/pub/uploads/reports/'
    dest_dir = '/var/www/localhost/htdocs/map/reports'
    print 'Creating symlinks for %s -> %s' % (dest_dir, root_dir)
    os.symlink(root_dir,dest_dir)
    print 'Successfully created symlinks'


def update_httpd_settings():
    print '\nSetting httpd DocumentRoot to /var/www/localhost/htdocs/map'
    os.chmod('/etc/phpmyadmin/config.inc.php', 0644)
    for line in fileinput.input('/etc/apache2/httpd.conf', inplace=True):
        print line.replace(
            'DocumentRoot "/var/www/localhost/htdocs"',
            'DocumentRoot "/var/www/localhost/htdocs/map"'),

def process_control():
    server = xmlrpclib.Server('http://localhost:9001/RPC2')
    print '\nRestarting httpd with supervisor'
    server.supervisor.stopProcess('httpd')
    server.supervisor.startProcess('httpd')
    print 'Starting map with supervisor'
    server.supervisor.startProcess('map')


if __name__ == "__main__":

    # 1. Get and save keys
    store_keys(get_keys())

    # 2. Set correct permissions for config file
    set_config_perms()

    # 3. Download the repos
    os.chdir('/home')
    clone_repo('bdt')
    clone_repo('robotframework')

    # 4. Import map_db
    import_map_db()

    # 5. Create front end symbolic links
    create_symlinks()

    # 6. Update httpd settings
    update_httpd_settings()

    # 7. Restart/start supervisor processes
    process_control()

    print "\nYou're all set!\n"

