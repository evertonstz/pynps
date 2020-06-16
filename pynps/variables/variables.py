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
VERSION = '1.6.1'

##STATIC DICTS AND LISTS##
FULL_SYSTEM_NAME = {"PSV": "Playstation Vita", "PSP": "Playstation Portable",
                     "PSX": "Playstation", "PSM": "Playstation Mobile", "PS3":"Playstation 3"}

SUFFIXES = ['bytes', 'KiB', 'MiB', 'GiB',
             'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

TYPE_DICT = {"GAMES": "Game", "THEMES": "Theme",
              "DLCS": "DLC", "DEMOS": "Demo", "UPDATES": "Update", "AVATARS": "Avatar"}

REGION_DICT = {"US": "USA", "EU": "EUR", "JP": "JAP", "ASIA": "ASIA",
                "INT": "INT", "usa": "US", "jap": "JP", "eur": "EU",
                "asia": "ASIA", "int": "INT", "all":"all"}

ORDER_DIC = {"c":"System", "console":"System",
                "id":"Title ID", "title_id":"Title ID",
                "r":"Region", "region":"Region",
                "t":"Type", "type":"Type",
                "n":"Name", "game_name":"Name",
                "s":"File Size", "size":"File Size"}

CONF_PSV_LINKS = {'games': 'https://nopaystation.com/tsv/PSV_GAMES.tsv',
                        'dlcs': 'https://nopaystation.com/tsv/PSV_DLCS.tsv',
                        'themes': 'https://nopaystation.com/tsv/PSV_THEMES.tsv',
                        'updates': 'https://nopaystation.com/tsv/PSV_UPDATES.tsv',
                        'demos': 'https://nopaystation.com/tsv/PSV_DEMOS.tsv'
                   }

CONF_PSP_LINKS = {'games': 'https://nopaystation.com/tsv/PSP_GAMES.tsv',
                        'dlcs': 'https://nopaystation.com/tsv/PSP_DLCS.tsv',
                        'themes': 'https://nopaystation.com/tsv/PSP_THEMES.tsv',
                        'updates': 'https://nopaystation.com/tsv/PSP_UPDATES.tsv'
                   }

CONF_PSX_LINKS = {'games': 'https://nopaystation.com/tsv/PSX_GAMES.tsv'
                   }

CONF_PSM_LINKS = {'games': 'https://nopaystation.com/tsv/PSM_GAMES.tsv'
                   }
CONF_PS3_LINKS = {'games': 'https://nopaystation.com/tsv/PS3_GAMES.tsv',
                        'dlcs': 'https://nopaystation.com/tsv/PS3_DLCS.tsv',
                        'themes': 'https://nopaystation.com/tsv/PS3_THEMES.tsv',
                        'demos': 'https://nopaystation.com/tsv/PS3_DEMOS.tsv',
                        'avatars':'https://nopaystation.com/tsv/PS3_AVATARS.tsv'
                   }
