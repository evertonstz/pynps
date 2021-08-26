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
import csv
from io import StringIO

import requests

from pynps.entities.games import Game


def _replace_dict_key_names(dictionary: dict[str, str]) -> dict[str, str]:
    replace_dict = {
        "Title ID": "game_id",
        "Region": "region",
        "Name": "name",
        "Original name": "original_name",
        "Original Name": "original_name",
        "PKG direct link": "pkg_direct_link",
        "RAP": "rap",
        "Content ID": "content_id",
        "Last Modification Date": "last_modified_date",
        "Download .RAP file": "rap_direct_link",
        "Download .rap file": "rap_direct_link",
        "File Size": "file_size",
        "SHA256": "sha256",
        "Required FW": "required_fw",
        "App Version": "app_version",
        "zRIF": "zrif",
        "Type": None,
    }

    for old, new in replace_dict.items():
        if new == None and old in dictionary:
            dictionary.pop(old)

        if old in dictionary:
            dictionary[new] = dictionary.pop(old)

    return dictionary


def _construct_Games_from_tsv_content(
    platform: str, type: str, content: str
) -> list[Game]:
    csv_reader = csv.DictReader(
        StringIO(content), delimiter="\t", quoting=csv.QUOTE_NONE
    )

    game_list: list[Game] = []
    for g in csv_reader:
        g = _replace_dict_key_names(g)
        g["platform"] = platform
        g["type"] = type
        game_list.append(Game(**g))

    return game_list


def _request_tsv_file(url: str) -> str:
    """download a file to a variable"""
    req = requests.get(url)
    return req.content.decode("utf-8")


def download_and_process_tsv_file(url: str, platform: str, type: str) -> list[Game]:
    """this function will use requests to download a given tsv file and dump it to a list of Game objects, making it basically stateless"""
    content = _request_tsv_file(url)
    return _construct_Games_from_tsv_content(platform, type, content)
