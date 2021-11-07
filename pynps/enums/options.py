from enum import Enum

class BaseSystemOptions(Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

class Options(Enum):
    GAMES = "GAMES"
    DLCS = "DLCS"
    THEMES = "THEMES"
    UPDATES = "UPDATES"
    DEMOS = "DEMOS"
    AVATARS = "AVATARS"

class PsvOptions(BaseSystemOptions):
    GAMES = Options.GAMES
    DLCS = Options.DLCS
    THEMES = Options.THEMES
    UPDATES = Options.UPDATES
    DEMOS = Options.DEMOS
    
class PspOptions(BaseSystemOptions):
    GAMES = Options.GAMES
    DLCS = Options.DLCS
    THEMES = Options.THEMES
    UPDATES = Options.UPDATES

class PsxOptions(BaseSystemOptions):
    GAMES = Options.GAMES

class PsmOptions(BaseSystemOptions):
    GAMES = Options.GAMES

class Ps3Options(BaseSystemOptions):
    GAMES = Options.GAMES
    DLCS = Options.DLCS
    THEMES = Options.THEMES
    DEMOS = Options.DEMOS
    AVATARS = Options.AVATARS