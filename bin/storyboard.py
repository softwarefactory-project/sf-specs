#! /usr/bin/env python

import argparse
import yaml
import os
import sys
from six.moves.urllib.parse import urljoin

from pysflib.sfauth import get_cookie
from pysflib.sfstoryboard import SFStoryboard
from storyboardclient._apiclient import exceptions


parser = argparse.ArgumentParser(description="Storyboard converter")
parser.add_argument('--url', '-u', metavar='https://sf.dom',
                    help='the URL of the SF instance')
parser.add_argument('--auth', '-a', nargs='?', metavar='username:password',
                    help='regular authentication', default=None)
parser.add_argument('--api-key', '-k', nargs='?', metavar='APIKEY',
                    help='API key authentication', default=None)

args = parser.parse_args()
if not args.auth and not args.api_key:
    sys.exit('Missing authentication')

if args.auth:
    if ':' not in args.auth:
        sys.exit('auth must be in the form username:password')
    user, password = args.auth.split(':')
    cookie = get_cookie(args.url, username=user, password=password)
else:
    cookie = get_cookie(args.url, api_key=args.api_key)

sbclient = SFStoryboard(urljoin(args.url, "storyboard_api"), cookie)


for root, dirnames, filenames in os.walk('../stories'):
    for f in filenames:
        full_path = os.path.join(root, f)
        epic = full_path.replace('../stories', '').replace(f, '').strip('/')
        # assuming validator was run before
        story = yaml.load(open(full_path))
        if epic:
            story['description'] += '\n\nThis story is part of epic: *%s*' % epic
        try:
            sbstory = sbclient.stories.find(title=story['title'])
            print "Story '%s' already exists." % story['title']
        except exceptions.NotFound:
            print "Creating story '%s'" % story['title']
            sbstory = sbclient.stories.create(title=story['title'],
                                              description=story['description'])
        for task in story['tasks']:
            try:
                sbtask = sbstory.tasks.find(title=task['title'])
                print "- Task '%s' already exists." % task['title']
            except exceptions.NotFound:
                # TODO add a check on project names in check pipeline
                prjs = sbclient.projects.get_all(name=task['project'])
                # needed due to $prj-distgit madness
                prj_id = [p.id for p in prjs if p.name == task['project']][0]
                sbstory.tasks.create(title=task['title'], project_id=prj_id)
                print "- Task '%s' created" % task['title']
        tags = []
        if epic and epic not in sbstory.tags:
            tags.append(epic)
        if 'groomed' not in sbstory.tags:
            tags.append('groomed')
        if tags:
            sbclient.put("tags/%s" % sbstory.id, json=tags)

print "Stories created or updated"
