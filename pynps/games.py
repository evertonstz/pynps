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


@dataclass
class Game:
    game_id: str
    platform: str
    type: str
    region: str = field(default="")
    name: str = field(default="")
    pkg_direct_link: str = field(default="")
    zrif: str = field(default="")
    content_id: str = field(default="")
    last_modified_date: str = field(default="")
    original_name: str = field(default="")
    sha256: str = field(default="")
    file_size: str = field(default="")
    app_version: str = field(default="")
    required_fw: str = field(default="")
    rap: str = field(default="")
    rap_direct_link: str = field(default="")