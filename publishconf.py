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
SITESUBTITLE = 'A JAPANESE BLOG by GUCHIO! <br>About : <a href="https://guchio3.github.io/guchiBLO/pages/AUTHOR.html">AUTHOR</a>, <a href="https://guchio3.github.io/guchiBLO/pages/CONTENTS.html">CONTENTS</a> <br>Categories : <a href="/category/machinelearning.html">Machine Learning</a>, <a href="/category/cryptocurrency.html">Crypto Currency</a>, etc..'
SITELOGO = '/images/siteBaseImages/guchiBLO_temp.png'
SITELOGO_SIZE = 200
FAVICON = SITEURL + '/images/siteBaseImages/favicon.ico'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
#PYGMENTS_STYLE = 'colorful'
