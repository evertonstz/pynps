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
import sys
from pynps.db import Database, GameDatabase
from pynps.configuration import Configurations
from commands.data.cli_options import CliOptions
import csv
from io import StringIO
from pynps.utils.progressbar import ProgressBar

import requests

from pynps.entities.games import Game
from rich.progress import Progress, TaskID


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
        "Update Version": None, #TODO add this to database? Belongs to PSV Update file
        "Required FW VERSION": None #TODO add this to database? Belongs to PSV Update file
    }

    for old, new in replace_dict.items():
        if new == None and old in dictionary:
            dictionary.pop(old)

        if old in dictionary:
            dictionary[new] = dictionary.pop(old)

    return dictionary


def _construct_Games_from_tsv_content(
    system: str, type: str, content: str
) -> list[Game]:
    # csv.field_size_limit(sys.maxsize)
    csv_reader = csv.DictReader(
        StringIO(content), delimiter="\t", quoting=csv.QUOTE_NONE
    )

    game_list: list[Game] = []
    for g in csv_reader:
        g = _replace_dict_key_names(g)
        g["platform"] = system
        g["type"] = type
        game_list.append(Game(**g))

    return game_list


def _request_tsv_file(url: str, system: str, type: str) -> str:
    """download a file to a variable"""
        
    chunks = []
    with Progress(expand=True) as progress:
        with requests.get(url, stream=True) as req:
            total_length = req.headers.get("content-length")

            total_length = int(req.headers.get("content-length", 0))

            prog_bar = ProgressBar(progress)
            prog_bar.add_url(url)
            prog_bar.add_total_size(total_length)
            prog_bar.add_description(
                f"[red]Downloading {system.upper()} {type.upper()} file..."
            )
            prog_bar.init_progress_bar()

            for chunk in req.iter_content(chunk_size=1024):
                prog_bar.update_progress_bar(url, advance_chunk=1024)
                chunks.append(chunk)

    return b"".join(chunks).decode("utf-8")

def download_and_process_tsv_file(url: str, system: str, type: str) -> list[Game]:
    """this function will use requests to download a given tsv file and dump it to a list of Game objects, making it basically stateless"""
    content = _request_tsv_file(url, system, type)
    return _construct_Games_from_tsv_content(system, type, content)

def _commit_list_of_Game_to_database(db: GameDatabase, list_games: list[Game]) -> None:
    for game in list_games:
        db.upsert(game)
    db.commit()

def update(system, cli_options: CliOptions, conf_file: Configurations, db: GameDatabase) -> None:
    for type, active in cli_options._asdict().items():
        if active:
            system_url_dict = conf_file.get_links_by_system_name(system)
            url = system_url_dict.get_url_by_type_name(type)
            list_games = download_and_process_tsv_file(url, system, type)

            _commit_list_of_Game_to_database(db, list_games)
