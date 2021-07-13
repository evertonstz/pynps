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

import configparser
import os
from dataclasses import dataclass, field
from shutil import Error
from typing import ClassVar

import pynps.consoles as consoles


@dataclass
class Path:
    path: str

    def __str__(self):
        return self.path

    def _fix_folder_syntax(self, path: str) -> str:
        """this function is used to fix slashes in the directories"""
        if "\\" in path:
            path = path.replace("\\", "/")
        if path.endswith("/"):
            path = path[:-1]

        return path

    def _unrapper(self, path: str, maindir: str) -> str:
        """this function is used to replace ./ with a full path to a file or folder"""
        if path.startswith("./"):
            path = f"{maindir}/{path[2:]}"
        return path

    def unrap(self, maindir: str) -> str:
        """when used a dot to express the script dir, the folder string needs to be unraped to express the full directory path"""
        return self._fix_folder_syntax(self._unrapper(self.path, maindir))


@dataclass(frozen=False)
class Configurations:
    """define the class used to interact with configuration parameters and the configuration file"""

    path: str
    download_folder: ClassVar[Path] = field(default=Path("./pynps_downloads/"))
    database_folder: ClassVar[Path] = field(default=Path("./pynps_database/"))
    pkg2zip_location: ClassVar[Path] = field(default=Path("./pynps_config/lib/pkg2zip"))
    wget_location: ClassVar[Path] = field(default=Path("./pynps_config/lib/wget"))
    psv_links: ClassVar[consoles.PsvConsoleTsvs] = field(
        default=consoles.PsvConsoleTsvs(
            games="http://nopaystation.com/tsv/PSV_GAMES.tsv",
            dlcs="http://nopaystation.com/tsv/PSV_DLCS.tsv",
            themes="http://nopaystation.com/tsv/PSV_THEMES.tsv",
            updates="http://nopaystation.com/tsv/PSV_UPDATES.tsv",
            demos="http://nopaystation.com/tsv/PSV_DEMOS.tsv",
        )
    )
    psp_links: ClassVar[consoles.PspConsoleTsvs] = field(
        default=consoles.PspConsoleTsvs(
            games="http://nopaystation.com/tsv/PSP_GAMES.tsv",
            dlcs="http://nopaystation.com/tsv/PSP_DLCS.tsv",
            themes="http://nopaystation.com/tsv/PSP_THEMES.tsv",
            updates="http://nopaystation.com/tsv/PSP_UPDATES.tsv",
        )
    )
    psx_links: ClassVar[consoles.PsxConsoleTsvs] = field(
        default=consoles.PsxConsoleTsvs(
            games="http://nopaystation.com/tsv/PSX_GAMES.tsv"
        )
    )
    psm_links: ClassVar[consoles.PsmConsoleTsvs] = field(
        default=consoles.PsmConsoleTsvs(
            games="http://nopaystation.com/tsv/PSM_GAMES.tsv"
        )
    )
    ps3_links: ClassVar[consoles.Ps3ConsoleTsvs] = field(
        default=consoles.Ps3ConsoleTsvs(
            games="https://nopaystation.com/tsv/PS3_GAMES.tsv",
            dlcs="https://nopaystation.com/tsv/PS3_DLCS.tsv",
            themes="https://nopaystation.com/tsv/PS3_THEMES.tsv",
            demos="https://nopaystation.com/tsv/PS3_DEMOS.tsv",
            avatars="https://nopaystation.com/tsv/PS3_AVATARS.tsv",
        )
    )

    __config = configparser.ConfigParser()

    def __post_init__(self):
        self.__config["pyNPS"] = {
            "DownloadFolder": self.download_folder,
            "DatabaseFolder": self.database_folder,
        }

        self.__config["BinaryLocations"] = {
            "Pkg2zip_Location": self.pkg2zip_location,
            "Wget_location": self.wget_location,
        }

        self.__config["PSV_Links"] = self.psv_links.__dict__
        self.__config["PSP_Links"] = self.psp_links.__dict__
        self.__config["PSX_Links"] = self.psx_links.__dict__
        self.__config["PSM_Links"] = self.psm_links.__dict__
        self.__config["PS3_Links"] = self.ps3_links.__dict__

    def _check_sections(self, parser: configparser.ConfigParser) -> bool:
        """checks if all sections are avaliable in a given list"""
        sections = parser.sections()

        obligatory_main_sections = [
            "pyNPS",
            "PSV_Links",
            "PSP_Links",
            "PSX_Links",
            "PSM_Links",
            "PS3_Links",
            "BinaryLocations",
        ]
        obligatory_psv_sections = ["games", "dlcs", "themes", "updates", "demos"]
        obligatory_psp_sections = ["games", "dlcs", "themes", "updates"]
        obligatory_psx_sections = ["games"]
        obligatory_psm_sections = ["games"]
        obligatory_ps3_sections = ["games", "dlcs", "themes", "demos", "avatars"]

        if sorted(sections) == sorted(obligatory_main_sections):
            if sorted(list(parser["PSV_Links"])) != sorted(obligatory_psv_sections):
                return False

            if sorted(list(parser["PSP_Links"])) != sorted(obligatory_psp_sections):
                return False

            if sorted(list(parser["PSX_Links"])) != sorted(obligatory_psx_sections):
                return False

            if sorted(list(parser["PSM_Links"])) != sorted(obligatory_psm_sections):
                return False
            if sorted(list(parser["PS3_Links"])) != sorted(obligatory_ps3_sections):
                return False

            return True
        else:
            return False

    def commit_to_file(self) -> None:
        """commit all attributes to configfile"""
        with open(self.path, "w") as file:
            self.__config.write(file)

    def read_from_file(self) -> None:
        """pull new information from the config file into this class' attributes"""
        self.__config.read(self.path)

        if os.path.isfile(self.path) == False:
            raise FileNotFoundError

        if self._check_sections(self.__config):
            self.download_folder = self.__config["pyNPS"]["downloadfolder"]
            self.database_folder = self.__config["pyNPS"]["databasefolder"]
            self.pkg2zip_location = self.__config["BinaryLocations"]["pkg2zip_location"]
            self.wget_location = self.__config["BinaryLocations"]["wget_location"]
            self.psv_links = consoles.PsvConsoleTsvs(**dict(self.__config["PSV_Links"]))
            self.psp_links = consoles.PspConsoleTsvs(**dict(self.__config["PSP_Links"]))
            self.psx_links = consoles.PsxConsoleTsvs(**dict(self.__config["PSX_Links"]))
            self.psm_links = consoles.PsmConsoleTsvs(**dict(self.__config["PSM_Links"]))
            self.ps3_links = consoles.Ps3ConsoleTsvs(**dict(self.__config["PS3_Links"]))
        else:
            raise Error(
                "unable to read the configuration file, check the syntax in the file and try again"
            )
