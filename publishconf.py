#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://guchio3.github.io/guchiBLO'
#SITELOGO = SITEURL + '/images/siteBaseImages/profile.png'
#SITELOGO = SITEURL + '/images/siteBaseImages/guchiBLO.png'
SITELOGO = '/images/siteBaseImages/guchiBLO.png'
FAVICON = SITEURL + '/images/siteBaseImages/favicon.ico'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
#PYGMENTS_STYLE = 'colorful'
