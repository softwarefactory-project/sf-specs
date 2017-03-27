#! /usr/bin/env python

import yaml
import os
import sys

for root, dirnames, filenames in os.walk('../stories'):
    for f in filenames:
        try:
            story = yaml.load(open(os.path.join(root, f)))
        except:
            sys.exit('%s is not a valid YAML file' % os.path.join(root, f))
        u = os.path.join(root, f)
        print u.replace('../stories/', '').replace('/' + f, '')
        if 'title' not in story:
            sys.exit('%s needs a title' % os.path.join(root, f))
        if 'description' not in story or story['description'] == '':
            sys.exit('%s needs a description' % os.path.join(root, f))
        if 'tasks' not in story or len(story['tasks']) < 1:
            sys.exit('%s needs at least one task' % os.path.join(root, f))
print 'User stories validated'
