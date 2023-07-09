#!/usr/bin/python3
"""
Fabric script to create archive of web_static directory
"""


from fabric.api import local
from datetime import datetime


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
