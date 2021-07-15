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
from dataclasses import dataclass, field
import typing


# this is guetto but works, hopefully god will forgive me
if __name__ == "__main__":
    import games
else:
    import pynps.games as games


@dataclass
class Database:
    path: str
    table: str

    def __post_init__(self):
        self.con = sqlite3.connect(self.path)
        self.con.row_factory = self._dict_factory

        # TODO check if table exists, if not, create it

    def _touch_table(self) -> None:
        cur = self.con.cursor()
        cur.execute(
            f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
		Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		GameId TEXT UNIQUE,		
		Platform TEXT NOT NULL,
		Type TEXT NOT NULL,
		Region TEXT,
		Name TEXT,
		ZRif TEXT,
		ContentId TEXT,
		LastModDate TEXT,
		OriginalName TEXT,
		Sha256 TEXT,
		FileSize INTEGER,
		AppVersion INTEGER,
		RequiredFw TEXT
	  );"""
        )

    def close(self) -> None:
        self.con.close()

    def commit(self) -> None:
        self.con.commit()

    def rollback(self) -> None:
        self.con.rollback()

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def query_all(self):
        cur = self.con.cursor()
        query = cur.execute(f"""SELECT * FROM {self.table};""")

        res = [
            games.Game(
                game_id=row["GameId"],
                platform=row["Platform"],
                type=row["Type"],
                region=row["Region"],
                name=row["Name"],
                zrif=row["ZRif"],
                content_id=row["ContentId"],
                last_modified_date=row["LastModDate"],
                original_name=row["OriginalName"],
                sha256=row["Sha256"],
                file_size=row["FileSize"],
                app_version=row["AppVersion"],
                required_fw=row["RequiredFw"],
            )
            for row in query
        ]

        return res


@dataclass
class Resumes(Database):
    pass


@dataclass
class GameDatabase(Database):
    def upsert(self, game: games.Game) -> None:
        cur = self.con.cursor()
        t = cur.execute(
            f"""
		INSERT INTO {self.table} (GameId, Platform, Type, Region, Name, ZRif, ContentId, LastModDate, OriginalName, Sha256, FileSize, AppVersion, RequiredFw)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(GameId) DO UPDATE SET
		Platform=excluded.Platform,
		Type=excluded.Type,
		Region=excluded.Region,
		Name=excluded.Name,
		ZRif=excluded.ZRif,
		ContentId=excluded.ContentId,
		LastModDate=excluded.LastModDate,
		OriginalName=excluded.OriginalName,
		Sha256=excluded.Sha256,
		FileSize=excluded.FileSize,
		AppVersion=excluded.AppVersion,
		RequiredFw=excluded.RequiredFw;""",
            (
                game.game_id,
                game.platform,
                game.type,
                game.region,
                game.name,
                game.zrif,
                game.content_id,
                game.last_modified_date,
                game.original_name,
                game.sha256,
                str(game.file_size),
                str(game.app_version),
                game.required_fw,
            ),
        )

        # TODO add option for autocommit


def main():
    # d = GameDatabase("D:/Documentos/GitHub/pynps/testfiles/test.db", "resumes")
    pass


if __name__ == "__main__":
    main()
