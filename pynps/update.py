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


def _construct_Game_from_tsv_row(system: str, type: str, row: list[str]) -> Game:
    if system == "psv":
        return Game(
            **{
                "game_id": row[0],
                "platform": system,
                "type": type,
                "region": row[1],
                "name": row[2],
                "pkg_direct_link": row[3],
                "zrif": row[4],
                "content_id": row[5],
                "last_modified_date": row[6],
                "original_name": row[7],
                "file_size": row[8],
                "sha256": row[9],
                "required_fw": row[10],
                "app_version": row[11],
            }
        )
    elif system == "psp":
        return Game(
            **{
                "game_id": row[0],
                "platform": system,
                "type": type,
                "region": row[1],
                "name": row[3],
                "pkg_direct_link": row[4],
                "content_id": row[5],
                "last_modified_date": row[6],
                "rap": row[7],
                "rap_direct_link": row[8],
                "file_size": row[9],
                "sha256": row[10],
            }
        )
    elif system == "psx":
        return Game(
            **{
                "game_id": row[0],
                "platform": system,
                "type": type,
                "region": row[1],
                "name": row[2],
                "pkg_direct_link": row[3],
                "content_id": row[4],
                "last_modified_date": row[5],
                "original_name": row[6],
                "file_size": row[7],
                "sha256": row[8],
            }
        )
    elif system == "psm":
        return Game(
            **{
                "game_id": row[0],
                "platform": system,
                "type": type,
                "region": row[1],
                "name": row[2],
                "pkg_direct_link": row[3],
                "zrif": row[4],
                "content_id": row[5],
                "last_modified_date": row[6],
                "file_size": row[7],
                "sha256": row[8],
            }
        )
    else:  # else is ps3
        return Game(
            **{
                "game_id": row[0],
                "platform": system,
                "type": type,
                "region": row[1],
                "name": row[2],
                "pkg_direct_link": row[3],
                "rap": row[4],
                "content_id": row[5],
                "last_modified_date": row[6],
                "rap_direct_link": row[7],
                "file_size": row[8],
                "sha256": row[9],
            }
        )


def download_and_process_tsv_file(url: str, system: str, type: str) -> list[Game]:
    """this function will use requests to download a given tsv file and dump it to a list of Game objects, making it basically stateless"""
    req = requests.get(url)
    content = req.content.decode("utf-8")

    data: list = []
    for index, row in enumerate(reader(content.splitlines(), delimiter="\t")):
        if index != 0:
            data.append(_construct_Game_from_tsv_row(system, type, row))

    return data
