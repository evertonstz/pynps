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
import sqlite3
from dataclasses import dataclass
from sqlite3.dbapi2 import Cursor
from typing import Any


# this is guetto but works, hopefully god will forgive me
if __name__ == "__main__":
    from games import Game
else:
    from pynps.games import Game


@dataclass
class Database:
    path: str
    table: str

    def __post_init__(self):
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = self._query_factory
        self._cursor = self._conn.cursor()

        # TODO check if table exists, if not, create it

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def _query_factory(self, cursor: Cursor, row: tuple) -> dict[str, Any]:
        """this is used by connection's row_factory method so it knows every row should return as a dict instead of atuple"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _query_to_games(self, query: Cursor):
        """this is used to convert the list of dicts that results from a query into a list of Game objects"""
        return [
            Game(
                game_id=row["game_id"],
                platform=row["platform"],
                type=row["type"],
                region=row["region"],
                name=row["name"],
                pkg_direct_link=row["pkg_direct_link"],
                zrif=row["zrif"],
                content_id=row["content_id"],
                last_modified_date=row["last_modified_date"],
                original_name=row["original_name"],
                sha256=row["sha256"],
                file_size=row["file_size"],
                app_version=row["app_version"],
                required_fw=row["required_fw"],
                rap=row["rap"],
                rap_direct_link=row["rap_direct_link"],
            )
            for row in query
        ]

    def close(self) -> None:
        self._conn.close()

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def touch_table(self) -> None:
        self._cursor.execute(
            f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
		    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    game_id TEXT UNIQUE,		
		    platform TEXT NOT NULL,
		    type TEXT NOT NULL,
		    region TEXT,
		    name TEXT,
            pkg_direct_link TEXT,
		    zrif TEXT,
		    content_id TEXT,
		    last_modified_date TEXT,
		    original_name TEXT,
		    sha256 TEXT,
		    file_size TEXT,
		    app_version TEXT,
		    required_fw TEXT,
            rap TEXT,
            rap_direct_link TEXT
	    );"""
        )

    def query_all(self) -> list[Game]:
        query = self._cursor.execute(f"""SELECT * FROM {self.table};""")
        return self._query_to_games(query)


@dataclass
class Resumes(Database):
    pass


@dataclass
class GameDatabase(Database):
    def upsert(self, game: Game) -> None:
        """this method upserts the data from a Game object into the sqlite3 database"""
        cur = self._conn.cursor()
        t = cur.execute(
            f"""
		INSERT INTO {self.table} (game_id, platform, type, region, name, pkg_direct_link, zrif, content_id, last_modified_date, original_name, sha256, file_size, app_version, required_fw, rap, rap_direct_link)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(game_id) DO UPDATE SET
		platform=excluded.platform,
		type=excluded.type,
		region=excluded.region,
		name=excluded.name,
        pkg_direct_link=excluded.pkg_direct_link,
		zrif=excluded.zrif,
		content_id=excluded.content_id,
		last_modified_date=excluded.last_modified_date,
		original_name=excluded.original_name,
		sha256=excluded.sha256,
		file_size=excluded.file_size,
		app_version=excluded.app_version,
		required_fw=excluded.required_fw,
        rap=excluded.rap,
        rap_direct_link=excluded.rap_direct_link;""",
            (
                game.game_id,
                game.platform,
                game.type,
                game.region,
                game.name,
                game.pkg_direct_link,
                game.zrif,
                game.content_id,
                game.last_modified_date,
                game.original_name,
                game.sha256,
                game.file_size,
                game.app_version,
                game.required_fw,
                game.rap,
                game.rap_direct_link,
            ),
        )

        # TODO add option for autocommit
