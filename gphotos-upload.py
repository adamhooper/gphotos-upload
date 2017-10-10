#!/usr/bin/env python3
"""Uploads .jpg files in a directory and its subdirectories to Google Photos.
"""

import argparse
import logging
import os
import os.path
import sys

from gphotos_upload import auth
from oauth2client import tools

def upload_directory_to_service(directory, service, full_quality = False):
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.JPEG'):
                path = os.path.join(dirpath, filename)
                service.ensure_file_uploaded(path, full_quality = full_quality)

def main():
    parser = argparse.ArgumentParser(description='Upload photos to Google Photos', parents=[ tools.argparser ])
    parser.add_argument('path', metavar='PATH', help='Path to directory containing .jpg files')
    parser.add_argument('--full-quality', help='Upload original resolution (counts against your storage quota)')

    args = parser.parse_args()

    logger = logging.getLogger('gphotos_upload')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))

    service = auth.login(args, logger)
    upload_directory_to_service(args.path, service, full_quality = args.full_quality)

if __name__ == '__main__':
    main()
