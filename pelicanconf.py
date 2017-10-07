#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'guchio3'
SITENAME = 'guchiBLO'
SITEURL = ''
HOME_PATH = os.environ['HOME']
PLUGIN_PATHS = [HOME_PATH+'/workspace/blog/pelican-plugins']
PLUGINS = ['render_math']
#SITELOGO = '/images/siteBaseImages/profile.png'
SITELOGO = '/images/siteBaseImages/guchiBLO.png'
SITELOGO_SIZE = '200'
SITESUBTITLE = 'A JAPANESE BLOG by GUCHIO (<a href="/pages/About.html">about</a>)'
FAVICON = SITEURL + '/images/siteBaseImages/favicon.ico'

COPYRIGHT_YEAR = 2017

PATH = 'content'
OUTPUT_PATH = 'docs'

TIMEZONE = 'Asia/Tokyo'
DEFAULT_DATE = 'fs'

DEFAULT_LANG = 'ja'

# theme
THEME = 'pelican-twitchy' 
#BOOTSTRAP_THEME = 'sandstone'
#PYGMENTS_STYLE = 'colorful'

# dateformat
#DEFAULT_DATE_FORMAT = '%Y-%m-%d'
#DEFAULT_DATE = 'fs'

#PAGE_SAVE_AS = ''
#ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
#ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Markdown settings
#MD_EXTENSIONS = ['linkify', 'del_ins', 'fenced_code', 'codehilite(css_class=highlight)', 'tables']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LOAD_CONTENT_CACHE = False

# Blogroll
LINKS = (
#         ('youtube', 'youtube.com'),
         )

# Social widget
SOCIAL = (
         ('twitter', 'https://twitter.com/ihcgT_Ykchi'),
#         ('facebook', 'https://www.facebook.com/taguchi.naoya?ref=bookmarks'),
         ('github', 'https://github.com/guchio3'),
         ('linkedin', 'https://www.linkedin.com/in/taguchi-naoya-545403121/'),
        )

DEFAULT_PAGINATION = 10

# Settings only for pelican-twitchy
HIDE_SITENAME = False


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
