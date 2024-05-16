#!/usr/bin/python3
"""Module to compress and archive the contents of web_static"""
from fabric.api import env, run, sudo, put, local, task


env.hosts = ['100.26.173.61', '34.224.62.106']
env.user = 'ubuntu'


def do_pack():
    """Function to archive content of web_static"""
    local('mkdir -p versions')
    archive_path = "versions/web_static_$(date +\'%Y%m%d%H%M%S\').tgz"
    result = local('tar -cvzf {} web_static'.format(archive_path))
    if result.succeeded:
        print(result)
        return archive_path
    else:
        return None
