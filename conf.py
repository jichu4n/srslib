# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#    Copyright (C) 2017 Chuan Ji <jichu4n@gmail.com>                          #
#                                                                             #
#    Licensed under the Apache License, Version 2.0 (the "License");          #
#    you may not use this file except in compliance with the License.         #
#    You may obtain a copy of the License at                                  #
#                                                                             #
#     http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                             #
#    Unless required by applicable law or agreed to in writing, software      #
#    distributed under the License is distributed on an "AS IS" BASIS,        #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
#    See the License for the specific language governing permissions and      #
#    limitations under the License.                                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sphinx documentation configuration.

Modified from sphix-quickstart.
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

project = 'srslib'
copyright = '2017, Chuan Ji'
author = 'Chuan Ji'

version = '0.1.4'
release = version

master_doc = 'index'
source_suffix = '.rst'
exclude_patterns = ['_docs', 'Thumbs.db', '.DS_Store', '.env', 'README.*']

pygments_style = 'sphinx'
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html',
    ]
}


