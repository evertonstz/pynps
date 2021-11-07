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
from pynps.configuration.constants import DEFAULT_DATABASE_FOLDER, DEFAULT_DOWNLOAD_FOLDER, DEFAULT_PKG2ZIP_PATH, DEFAULT_WGET_PATH, PS3_AVATARS_DEFAULT_URL, PS3_DEMOS_DEFAULT_URL, PS3_DLCS_DEFAULT_URL, PS3_GAMES_DEFAULT_URL, PS3_THEMES_DEFAULT_URL, PSM_GAMES_DEFAULT_URL, PSP_DLCS_DEFAULT_URL, PSP_GAMES_DEFAULT_URL, PSP_THEMES_DEFAULT_URL, PSP_UPDATES_DEFAULT_URL, PSV_DEMOS_DEFAULT_URL, PSV_DLCS_DEFAULT_URL, PSV_GAMES_DEFAULT_URL, PSV_THEMES_DEFAULT_URL, PSV_UPDATES_DEFAULT_URL, PSX_GAMES_DEFAULT_URL

from pynps.consoles import *


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


# TODO user shouldn't be forced to set every parameter in the config file, in cases like this, the parameter not available in the config file will be the default fields in this class
# TODO refact: unlink entity from business methods
@dataclass(frozen=False)
class Configurations:
    """define the class used to interact with configuration parameters and the configuration file"""

    path: str
    download_folder: Path = field(default=Path(DEFAULT_DOWNLOAD_FOLDER))
    database_folder: Path = field(default=Path(DEFAULT_DATABASE_FOLDER))
    pkg2zip_location: Path = field(default=Path(DEFAULT_PKG2ZIP_PATH))
    wget_location: Path = field(default=Path(DEFAULT_WGET_PATH))
    psv_links: PsvConsoleTsvs = field(
        default=PsvConsoleTsvs(
            games=PSV_GAMES_DEFAULT_URL,
            dlcs=PSV_DLCS_DEFAULT_URL,
            themes=PSV_THEMES_DEFAULT_URL,
            updates=PSV_UPDATES_DEFAULT_URL,
            demos=PSV_DEMOS_DEFAULT_URL,
        )
    )
    psp_links: PspConsoleTsvs = field(
        default=PspConsoleTsvs(
            games=PSP_GAMES_DEFAULT_URL,
            dlcs=PSP_DLCS_DEFAULT_URL,
            themes=PSP_THEMES_DEFAULT_URL,
            updates=PSP_UPDATES_DEFAULT_URL,
        )
    )
    psx_links: PsxConsoleTsvs = field(
        default=PsxConsoleTsvs(games=PSX_GAMES_DEFAULT_URL)
    )
    psm_links: PsmConsoleTsvs = field(
        default=PsmConsoleTsvs(games=PSM_GAMES_DEFAULT_URL)
    )
    ps3_links: Ps3ConsoleTsvs = field(
        default=Ps3ConsoleTsvs(
            games=PS3_GAMES_DEFAULT_URL,
            dlcs=PS3_DLCS_DEFAULT_URL,
            themes=PS3_THEMES_DEFAULT_URL,
            demos=PS3_DEMOS_DEFAULT_URL,
            avatars=PS3_AVATARS_DEFAULT_URL,
        )
    )

    __config = configparser.ConfigParser()

    def _populate___config_with_data_from_attributes(self):
        """populate __config object with the data from all the attributes"""
        self.__config["pyNPS"] = {
            "DownloadFolder": self.download_folder.path,
            "DatabaseFolder": self.database_folder.path,
        }

        self.__config["BinaryLocations"] = {
            "Pkg2zip_Location": self.pkg2zip_location.path,
            "Wget_location": self.wget_location.path,
        }

        self.__config["PSV_Links"] = self.psv_links.__dict__
        self.__config["PSP_Links"] = self.psp_links.__dict__
        self.__config["PSX_Links"] = self.psx_links.__dict__
        self.__config["PSM_Links"] = self.psm_links.__dict__
        self.__config["PS3_Links"] = self.ps3_links.__dict__

    def _check_sections(self, parser: configparser.ConfigParser) -> bool:
        """checks if all sections are avaliable in the on_disk configuration file"""
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
        """commit all attributes to on_disk configfile"""
        self._populate___config_with_data_from_attributes()

        with open(self.path, "w") as file:
            self.__config.write(file)

    def read_from_file(self) -> None:
        """pull new information from the config file into this class' attributes"""
        self.__config.read(self.path)

        if os.path.isfile(self.path) == False:
            raise FileNotFoundError(f"can't find {self.path} on disk")

        if self._check_sections(self.__config):
            self.download_folder.path = self.__config["pyNPS"]["downloadfolder"]
            self.database_folder.path = self.__config["pyNPS"]["databasefolder"]
            self.pkg2zip_location.path = self.__config["BinaryLocations"][
                "pkg2zip_location"
            ]
            self.wget_location.path = self.__config["BinaryLocations"]["wget_location"]
            self.psv_links = PsvConsoleTsvs(**dict(self.__config["PSV_Links"]))
            self.psp_links = PspConsoleTsvs(**dict(self.__config["PSP_Links"]))
            self.psx_links = PsxConsoleTsvs(**dict(self.__config["PSX_Links"]))
            self.psm_links = PsmConsoleTsvs(**dict(self.__config["PSM_Links"]))
            self.ps3_links = Ps3ConsoleTsvs(**dict(self.__config["PS3_Links"]))
        else:
            raise Error(
                "unable to read the configuration file, check the syntax in the file and try again"
            )

    def get_links_by_system_name(self, system: str) -> ConsoleTsvs:
        return getattr(self, f"{system}_links")