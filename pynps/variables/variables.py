#!/usr/bin/python3
# coding=utf-8
# Created by evertonstz
""" This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. """

# Versioning
VERSION = '1.4.2'

##STATIC DICTS AND LISTS##
FULL_SYSTEM_NAME = {"PSV": "Playstation Vita", "PSP": "Playstation Portable",
                     "PSX": "Playstation", "PSM": "Playstation Mobile"}

SUFFIXES = ['bytes', 'KiB', 'MiB', 'GiB',
             'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

TYPE_DICT = {"GAMES": "Game", "THEMES": "Theme",
              "DLCS": "DLC", "DEMOS": "Demo", "UPDATES": "Update"}

REGION_DICT = {"US": "USA", "EU": "EUR", "JP": "JAP", "ASIA": "ASIA",
                "INT": "INT", "usa": "US", "jap": "JP", "eur": "EU",
                "asia": "ASIA", "int": "INT", "all":"all"}

CONF_PSV_LINKS = {'games': 'http://nopaystation.com/tsv/PSV_GAMES.tsv',
                   'dlcs': 'http://nopaystation.com/tsv/PSV_DLCS.tsv',
                           'themes': 'http://nopaystation.com/tsv/PSV_THEMES.tsv',
                           'updates': 'http://nopaystation.com/tsv/PSV_UPDATES.tsv',
                           'demos': 'http://nopaystation.com/tsv/PSV_DEMOS.tsv'
                   }

CONF_PSP_LINKS = {'games': 'http://nopaystation.com/tsv/PSP_GAMES.tsv',
                   'dlcs': 'http://nopaystation.com/tsv/PSP_DLCS.tsv',
                           'themes': 'http://nopaystation.com/tsv/PSP_THEMES.tsv',
                           'updates': 'http://nopaystation.com/tsv/PSP_UPDATES.tsv'
                   }

CONF_PSX_LINKS = {'games': 'http://nopaystation.com/tsv/PSX_GAMES.tsv'
                   }

CONF_PSM_LINKS = {'games': 'http://nopaystation.com/tsv/PSM_GAMES.tsv'
                   }