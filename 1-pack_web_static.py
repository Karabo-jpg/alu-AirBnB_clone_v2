#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of web_static
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    Returns:
        Path to the archive if successful, None otherwise
    """
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Generate archive path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        # Create tar archive of web_static folder
        local("tar -cvzf {} web_static".format(archive_path))

        # Return archive path if successful
        if os.path.exists(archive_path):
            return archive_path
        return None
    except Exception:
        return None 