#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'guchio3'
SITENAME = 'guchiBLO'
SITEURL = ''
STATIC_PATHS = ['images']
HOME_PATH = os.environ['HOME']
PLUGIN_PATHS = [HOME_PATH+'/workspace/blog/pelican-plugins']
PLUGINS = ['render_math']

SITELOGO = '/images/siteBaseImages/guchiBLO_temp.png'
SITELOGO_SIZE = '200'
SITESUBTITLE = 'A JAPANESE BLOG by GUCHIO! <br>About : <a href="/pages/AUTHOR.html">AUTHOR</a>, <a href="/pages/CONTENTS.html">CONTENTS</a> <br> Interested in : <a href="/category/machinelearning.html">Machine Learning (機械学習)</a>, <a href="/category/cryptocurrency.html">Crypto Currency (仮想通貨)</a>, etc...'
FAVICON = SITEURL + '/images/siteBaseImages/favicon.ico'

COPYRIGHT_YEAR = 2017

PATH = 'content'
OUTPUT_PATH = 'docs'

TIMEZONE = 'Asia/Tokyo'
DEFAULT_DATE = 'fs'

#DEFAULT_LANG = 'ja'
DEFAULT_LANG = 'en'

# Google analitics
GOOGLE_ANALYTICS = 'UA-107917533-1'

# theme settings
THEME = 'pelican-twitchy' 
#BOOTSTRAP_THEME = 'sandstone'
#PYGMENTS_STYLE = 'colorful'
DISQUS_SITENAME = True
DISQUS_LOAD_LATER = False
#DISPLAY_TAGS_ON_MENU = True
#DISPLAY_TAGS_INLINE = True
#DISPLAY_RECENT_POSTS_ON_MENU = True

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
#         ('linkedin', 'https://www.linkedin.com/in/taguchi-naoya-545403121/'),
        )

DEFAULT_PAGINATION = 10

# Settings only for pelican-twitchy
HIDE_SITENAME = True


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
