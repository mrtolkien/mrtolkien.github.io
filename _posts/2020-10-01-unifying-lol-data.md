---
title: "Unifying League of Legends Data"
categories: Development
tags:
  - Esports
  - Python
  - Data
header:
  image: /assets/images/lol_dto.png
---

In my two years working on League of Legends data, I have acquired data from:

- The [Riot Games API](https://developer.riotgames.com/apis#match-v4/GET_getMatch)

- The [Leaguepedia API](https://lol.gamepedia.com/Help:API_Documentation)

- Community sites like [Oracle’s Elixir](https://oracleselixir.com/tools/downloads)

- Commercial APIs like [pandascore](https://pandascore.co/)

- Computer vision algorithms

- ORMs like [Cassiopeia](https://github.com/meraki-analytics/cassiopeia)

- Packages like [RoleML](https://github.com/Canisback/roleML)

Objects in those sources can all represent the same underlying League of Legends game but they use different data structures and nomenclatures. And to get full information about a game, you usually need to use multiple of those sources.

Despite that, the underlying League of Legends game is **unique**. Any kill, any player in a League of Legends game is an **indivisible piece of information** that should be the same across **all** data sources.

If we could all agree on a common data representation for LoL games, it would make everybody’s life easier. Inserting game objects into databases would require managing a single input format. Merging information from multiple sources would be painless. Analysis scripts would be able to use any data source. Newcomers would only need to get used to a single format and be able to start developing their own tools much faster.

# Moving towards unification

The truth is, I have been thinking about restructuring League of Legends game data ever since I came in contact with Riot’s API data format. Many things in the structure of their `MatchDto` and `MatchTimelineDto` do not make much sense and it makes parsing very error prone.

But the current story starts 4 months ago, when I finally made steps towards creating a unique format that could be shared by multiple data sources.

What I wanted most was to not create another useless standard.

![relevant xkcd](https://imgs.xkcd.com/comics/standards.png)

I therefore started by contacting diverse groups of people working with LoL data to make sure I included as many points of view as possible. This included:

- Developers from [Meraki Analytics](https://github.com/meraki-analytics)

- Developers from [Leaguepedia](https://lol.gamepedia.com/Help:API_Documentation)

- Rioters in charge of [data archiving](https://twitter.com/Antwhan)

- Data Scientists in [other esports teams](https://twitter.com/valens)

- Community members from the [Riot API discord server](https://discord.gg/riotgamesdevrel)

The people at Meraki in particular helped me craft an object that was as generic as possible and could easily be used by multiple programming languages and storage solutions while staying humanly readable.

# LolGame DTO

Early in the process, we decided the Data Transfer Object (DTO) to be:

- JSON-compliant

- Easily extensible

- Inspired by Riot’s `MatchDto` to make the transition easier

- As intuitive as possible

In particular, making the data format intuitive meant putting objects as close as possible to what they refer to.

After many iterations, we agreed on this data structure, showing only list and dictionary fields:
```
game: dict
├── sources: dict
├── teams: dict
│   ├── bans: list
│   ├── monstersKills: list
│   ├── buildingsKills: list
│   └── players: list
│       ├── uniqueIdentifiers: dict
│       ├── endOfGameStats: dict
│       │   └── items: list
│       ├── summonersSpells: list
│       ├── runes: list
│       ├── snapshots: list
│       ├── itemsEvents: list
│       ├── wardsEvents: list
│       └── skillsLevelUpEvents: list
├── kills: list
└── picks_bans: list
```

The rest of the data fields are defined in [the python `LolDto` reference implementation](https://github.com/mrtolkien/lol_dto/tree/master/lol_dto/classes/game) as well as [the README of the project](https://github.com/mrtolkien/lol_dto/blob/master/README.md).

This reference implementation offers a `TypedDict` class representing a `LolDto`, enabling auto-completion and linting in python IDEs. It also handles [merging multiple DTOs](https://github.com/mrtolkien/lol_dto/blob/master/lol_dto/utilities/merge_games.py#L51).

Regarding the new fields:

- `game[sources]`, `team[uniqueIdentifiers]`, and `player[uniqueIdentifiers]` contain unique identifiers for the data sources
	- Keys represent the data source, for example `game[sources][riot]` for the official LoL API
	- The keys in this dictionary depend in the data source. The Riot API needs a `gameId` as well as a `platformId` to identify a game for example.
- `game[kills]` is placed at the root of the `game` because it refers to multiple `players`
- `player[id]` is Riot’s API `participantId` and had to be kept to stay compatible with `MatchTimelineDto` objects which do not contain any other way to reference players
- `snapshots` represent full player information (gold, xp, position) at a given timestamp
- All game timestamps are in seconds but can be floats to allow millisecond precision

While development is still ongoing, [`lol-dto` is now officially released in its `1.0` version](https://pypi.org/project/lol-dto/) and new versions will strive to stay backwards compatible.

# Riot Transmute

But what good is a reference implementation if you cannot acquire data in this format?

Of course, my first priority was to make a tool that would convert Riot’s `MatchDto` and `MatchTimelineDto` to a `LolGame`, merging both Riot objects to a single convenient DTO.

This tool is [`riot-transmute`](https://github.com/mrtolkien/riot_transmute)

```python
import riot_transmute
import lol_dto

# match is a MatchDto acquired from /lol/match/v4/{matchId}
game_from_match = riot_transmute.match_to_game(match)

# match_timeline is a MatchTimelineDto acquired from /lol/match/v4/timelines/by-match/{matchId}
game_from_timeline = riot_transmute.match_timeline_to_game(match_timeline, game_id, platform_id)

full_game = lol_dto.utilities.merge_games(game_from_match, game_from_timeline)
```

[JSON examples can be found here](https://github.com/mrtolkien/riot_transmute/tree/master/json_examples) if you want to take a look at a [full `LolGame` object](https://github.com/mrtolkien/riot_transmute/blob/master/json_examples/game_merged_with_names.json) created from the two different objects available in Riot’s API.

It also supports the extra fields added inside the `MatchDto` by `roleml` for accurate role assignment.

# Leaguepedia Parser

The most popular source for League of Legends esports data is [Leaguepedia](https://lol.gamepedia.com/League_of_Legends_Esports_Wiki). It is the only accurate source for full picks and bans order as they are not included in Riot’s data.

Leaguepedia’s data is stored in [Cargo tables](https://lol.gamepedia.com/Special:CargoTables) which can be queried with an SQL-like language.

While it is very convenient for single-table queries, joining on multiple tables or using subqueries can be messy and the resulting data is always 2-dimensional as it is how SQL operates.

So I updated my existing [`leaguepedia-parser`](https://github.com/mrtolkien/leaguepedia_parser) for it to output `LolGame` objects instead of raw dictionaries:

```python
def get_games(tournament_overview_page=None, **kwargs) -> List[LolGame]:
    """Returns basic information about all games played in a tournament.

    Queried information includes match history URL, tournament name,
    	team names, start time, # in series, patch, vod link, winner,
    	object kills per team, and player names

    Args:
        tournament_overview_page: tournament overview page, acquired from get_tournaments().

    Returns:
        A list of LolGame objects containing basic game information.
    """
```

Afterwards, the `get_game_details(game: LolGame) -> LolGame` function can be used to add more information into the game object, including full picks and bans as well as player-specific information.

The modularity of the `LolGame` format is out in full force here. The same object can be injected with more and more data when new pieces of information are retrieved, making sure all data about the game is always contained in a single JSON-serializable object.

And when you retrieve the associated `MatchDto` and `MatchTimelineDto` objects, you can continue merging them into the existing `LolGame` to arrive at a unique representation of all the information you acquired about the game, which can then easily be dumped to your favorite storage service.

# Moving forward

I have been using `lol-dto`, `riot-transmute`, and `leaguepedia-parser` for 4 months and the parser I wrote for Leaguepedia also relies heavily on those packages. Every new match history information you see on Leaguepedia uses the `LolGame` format in the background to populate Leaguepedia Cargo tables.

This means that those three packages have been heavily tested in real-world conditions and can be safely used in your projects moving forward. And this also means I am currently looking for help to spread the good word and improve the tools around `LolGame`!

While those three packages are far from perfect they are at a good point to start building upon.

The next steps are to:

- Rewrite the `cassiopeia` back-end to use `LolGame` as the lead developers are OK with it but do not have the time to implement it

- Write documentation for the `LolGame` DTO dissociated from the python reference implementation

- Update `riot-transmute` to add compatibility with games played before season 8 and test them thoroughly

- Write a `Go` implementation of `riot-transmute` running a local API in Docker to allow for much faster parsing and easier compatibility with any programming language

My goal with this standard is to empower developers, simplify compatibility between community tools, and help new developers. I think switching over to this new data format is a net positive for everybody.

And with community support, we can make this switch happen!
