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
RELATIVE_URLS = False


AUTHOR = 'guchio3'
SITENAME = 'guchiBLO'
THEME = './themes/pelican-themes/Flex'
SITELOGO = SITEURL + '/images/siteBaseImages/profile.png'

COPYRIGHT_YEAR = 2017

PATH = 'content'
OUTPUT_PATH = 'docs'

TIMEZONE = 'Asia/Tokyo'
DEFAULT_DATE = 'fs'

DEFAULT_LANG = 'ja'


FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Blogroll
LINKS = (
         ('youtube', 'youtube.com'),
         )

# Social widget
SOCIAL = (
         ('twitter', 'https://twitter.com/ihcgT_Ykchi'),
#         ('facebook', 'https://www.facebook.com/taguchi.naoya?ref=bookmarks'),
         ('github', 'https://github.com/guchio3'),
#         ('linkedin', 'https://www.linkedin.com/in/taguchi-naoya-545403121/'),
        )

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
