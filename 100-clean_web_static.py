#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""


from fabric.api import *
from datetime import datetime
import os


env.hosts = ['34.237.91.139', '34.239.253.108']
env.user = "ubuntu"


def do_pack():
    """
    Packs the contents of web_static into a tgz archive
    """

    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Create the timestamp string
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the archive filename
        archive = f"web_static_{timestamp}.tgz"

        # Create the archive command
        command = f"tar -czf versions/{archive} web_static"

        # Create the archive
        local(command)

        # Return the path to the archive
        return f"versions/{archive}"
    except Exception:
        # Return None if there was an error
        return None


def do_deploy(archive_path):
    """
    Sends archive to server and deploys changes
    """

    # Validate archive_path
    if not os.path.exists(archive_path):
        return False

    try:
        # Variable & Path building
        archive = os.path.basename(archive_path)
        folder = archive.split('.')[0]
        tmp = f"/tmp/{archive}"
        releases = f"/data/web_static/releases/{folder}"

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, tmp)

        # Uncompress the archive in the releases path
        run(f"mkdir -p {releases}")
        run(f"tar -xzf {tmp} -C {releases}")
        run(f"rm {tmp}")
        run(f"mv {releases}/web_static/* {releases}")
        run(f"rm -rf {releases}/web_static")

        # Remove empty web_static dir
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to updated files
        run(f"ln -s {releases} /data/web_static/current")

        # Refresh permissions, ownership & nginx
        sudo("chown -R ubuntu:ubuntu /data/")
        sudo("chmod -R 755 /data/")
        sudo("service nginx restart")
    except Exception:
        return False


def deploy():
    """
	Create and distribute the web_static archive
	"""

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    ""
	"Deletes out-of-date archives
	"""

    number = int(number)
    
    if number in [0,1]:
        number = 1
    else:
        number += 1
    
    with lcd("versions"):
        local(f"ls -1t | tail -n +{numbet} | xargs rm -rf")

    with cd("/data/web_static/releases"):
        run(f"ls -1t | tail -n +{number} | xargs rm -rf")
