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
from csv import reader

import requests

from pynps.db import GameDatabase
from pynps.games import Game


def _replace_tsv_keys_with_keys_used_on_database(keys: list) -> list:
    """The .tsv files from nopaystation.com have column names that are incompatible with the names used in the Game class,
    mostly due to PEP8 naming conventions. This function is used from the nopaystation names to the ones used by this app"""
    new_keys = []
    for key in keys:
        if key == "Title ID":
            new_keys.append("game_id")  #
        elif key == "Region":
            new_keys.append("region")  #
        elif key == "Name":
            new_keys.append("name")  #
        elif key == "PKG direct link":
            new_keys.append("pkg_direct_link")  #
        elif key == "zRIF":
            new_keys.append("zrif")
        elif key == "Content ID":
            new_keys.append("content_id")
        elif key == "Last Modification Date":
            new_keys.append("last_modified_date")
        elif key == "File Size":
            new_keys.append("file_size")
        elif key == "SHA256":
            new_keys.append("sha256")
        elif key == "RAP":
            new_keys.append("rap")
        elif key == "Download .RAP file":
            new_keys.append("rap_direct_link")
        elif key == "Original Name":
            new_keys.append("original_name")
        elif key == "Required FW":
            new_keys.append("required_fw")
        elif key == "App Version":
            new_keys.append("app_version")

    return new_keys


def download_and_process_tsv_file(url: str, system: str, type: str) -> list[Game]:
    """this function will use requests to download a given tsv file and dump it to a list of Game objects, making it basically stateless"""
    req = requests.get(url)
    content = req.content.decode("utf-8")

    keys: list
    data: list = []
    for index, row in enumerate(reader(content.splitlines(), delimiter="\t")):
        if index == 0:  # builds key dictionary
            keys = _replace_tsv_keys_with_keys_used_on_database(row)
        else:
            # keys can't be unbound, so I'm teling the linter to ignore the next row
            data.append({key: value for key, value in zip(keys, row)})  # type: ignore

    # construct Game object
    games = [Game(**row, platform=system, type=type) for row in data]
    return games
