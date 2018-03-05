#!/usr/bin/python

import os
import subprocess
import sys
sys.path.append('/usr/local/munki')
from munkilib import FoundationPlist


def main():
    try:
        proc = subprocess.Popen(['/usr/local/bin/chef-client', '--version'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = proc.communicate()
        # Example return from stdout: Chef: 13.2.20 \n
        version = stdout.split(' ')[1]
        version = version.split('\n')[0]
    except (IOError, OSError):
        version = '0.0.0'

    plist_path = '/usr/local/sal/plugin_results.plist'

    if os.path.exists(plist_path):
        plist = FoundationPlist.readPlist(plist_path)
    else:
        plist = []
    result = {}
    result['plugin'] = 'ChefVersion'
    result['historical'] = False
    data = {}
    data['Version'] = version
    result['data'] = data
    plist.append(result)
    FoundationPlist.writePlist(plist, plist_path)


if __name__ == '__main__':
    main()
