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

def main():
    p = Ps3ConsoleTsvs(
            games="https://nopaystation.com/tsv/PS3_GAMES.tsv",
            dlcs="https://nopaystation.com/tsv/PS3_DLCS.tsv",
            themes="https://nopaystation.com/tsv/PS3_THEMES.tsv",
            demos="https://nopaystation.com/tsv/PS3_DEMOS.tsv",
            avatars="https://nopaystation.com/tsv/PS3_AVATARS.tsv",
        )
    
    print(p.avatars)

if __name__ == '__main__':
    main()
