#!/usr/bin/python3
"""Module to distribute an archive of the contents of web_static
    to the web servers
"""
from fabric.api import env, run, sudo, put, local, task
import os


env.hosts = ['100.26.173.61', '34.224.62.106']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Function to deploy archived content of web_static to web servers"""
    if os.path.exists(archive_path):
        archive_file_nopath = os.path.basename(archive_path)
        archive_path_noext = os.path.splitext(archive_file_nopath)[0]
        r1 = put('{}'.format(archive_path), '/tmp')
        r2 = run('mkdir -p /data/web_static/releases/{}/'
                 ''.format(archive_path_noext))
        r3 = run('tar -xzf /tmp/{}.tgz -C /data/web_static/'
                 'releases/{}/'.format(archive_path_noext, archive_path_noext))
        r4 = run('rm /tmp/{}.tgz'.format(archive_path_noext))
        r5 = run('mv /data/web_static/releases/{}/web_static/* '
                 '/data/web_static/releases/{}/'.format(archive_path_noext,
                                                        archive_path_noext))
        r6 = run('rm -rf /data/web_static/releases/{}/'
                 'web_static'.format(archive_path_noext))
        r7 = run('rm -rf /data/web_static/current')
        r8 = run('ln -s /data/web_static/releases/{}/ '
                 '/data/web_static/current'.format(archive_path_noext))
        if (r1.succeeded and r2.succeeded and r3.succeeded and r4.succeeded and
           r5.succeeded and r6.succeeded and r7.succeeded and r8.succeeded):
            return True
        else:
            return False
    else:
        return False
