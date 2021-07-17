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

from dataclasses import dataclass, field


@dataclass(frozen=False)
class ConsoleTsvs:
    games: str


@dataclass(frozen=False)
class PsvConsoleTsvs(ConsoleTsvs):
    dlcs: str
    themes: str
    updates: str
    demos: str


@dataclass(frozen=False)
class PspConsoleTsvs(ConsoleTsvs):
    dlcs: str
    themes: str
    updates: str


@dataclass(frozen=False)
class PsxConsoleTsvs(ConsoleTsvs):
    pass


@dataclass(frozen=False)
class PsmConsoleTsvs(ConsoleTsvs):
    pass


@dataclass(frozen=False)
class Ps3ConsoleTsvs(ConsoleTsvs):
    dlcs: str
    themes: str
    demos: str
    avatars: str
