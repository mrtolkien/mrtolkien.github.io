#!/usr/bin/env python
# coding: utf-8

# # Clustering Legends of Runeterra archetypes
# 
# ## Goal
# 
# Given a list of `n` [Legends of Runeterra](https://playruneterra.com/en-sg/) decks, how to automatically group them into **archetypes**, *ie* groups of similar decks?
# 
# Clustering decks as archetypes allows for better calculation of metrics like win-rate and play-rate. This is a problem that comes back for every card game I have ever played, and is usually "simply" solved by humans sort the decks themselves.
# 
# But what if deck clustering could be automated?
# 
# ## Approaches
# 
# ### Intuition
# 
# I started to think about how to "simply" group decklists. Two ways came to mind:
# 
# - Choosing decks that have a pool of common cards
# - Choosing decks that have few different cards
# 
# Whichever distance we choose, we can start from individual decks and add new decks one by one, selecting the "closest" one to the cluster at each step. We can do this process in descending popularity order, so ties are broken by the popularity of decks. We can then select the biggest non-overlapping clusters found as good archetypes and re-start the process.
# 
# It does sound pretty close to k-means as it also relies on a centroid vector for each cluster, but here we don't have to select how many clusters we want from the start. We can also have clusters of very different sizes and it will not be an issue with our approach.
# 
# We'll call that method **incremental constrained cluster growth** and it's the one I'll be implementing in this blog post.
# 
# ### Existing clustering algorithms
# 
# Clustery analysis is a complex and heavily researched domain. Algorithms usually exhibit `O(n**3)` complexity.
# 
# The most popular clustering algorithm, or at least the only one I remember from my M.Sc., is [k-means](https://en.wikipedia.org/wiki/K-means_clustering). It's unfortunately a pretty poor fit here as we don't know the number of archetypes/clusters we are looking for, and it's also poorly adapted for clusters of vastly different sizes.
# 
# [Hierarchical clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering) is a better fit for our use-case:
# 
# > In data mining and statistics, hierarchical clustering (also called hierarchical cluster analysis or HCA) is a method of cluster analysis which seeks to build a hierarchy of clusters.
# 
# Deck archetypes naturally have multiple levels of "granularity" we can look at. From big macro archetypes being defined only by a few cards to micro archetypes arising from very few card differences. Ordering them in a hierarchy sounds like a great fit even though it will be harder to use for visualisation and analysis.
# 
# I will try hierarchical clustering and visualisation at some point, but I'm keeping it for a future blog post!
# 

# ## Preparing data
# 
# ### Games selection
# 
# As Legends of Runeterra does not offer access to ranks through its API, I use [TrueSkill](https://trueskill.org/) to identify the best players on a given server and parse them in descending skill order. I only use ranked results to determine skill ratings.
# 
# I verified the algorithm by verifying that the best players identified by TrueSkill were indeed in Master rank. We can do that by checking account names, which is the only type of rank data available.
# 
# This allows me to parse games for the ~20 000 best players per server, which returns ~35 000 ranked games per day per server. As there are 3 servers in total, we have ~100 000 games per day of data. This likely covers rank until platinum, and maybe even gold. But we have no way to check as LoR's API doesn't let us query ranks for players ¯\\_(ツ)_/¯
# 
# ### SQL query
# 
# The data parsed from Riot's API is susceptible to regular model changes and I've therefore saved it as a `JSONB` column in `Postgres`.
# 
# I have written that query in many different ways but in the end making a subquery to create a `player` table was the easiest for me to maintain. I'm sure this query can be written in a smarter way but I'm still only starting to get used to `JSONB` direct querying with Postgres:
# 
# ```postgres
# SELECT
#   deck_code,
#   factions,
#   COUNT(*) as games,
#   COUNT(CASE WHEN win::boolean THEN 1 END) as wins
# FROM (
#   SELECT
#     jsonb_array_elements(lor_game.data->'info'->'players')->>'win' as win,
#     jsonb_array_elements(lor_game.data->'info'->'players')->>'deck_code' as deck_code,
#     jsonb_array_elements(lor_game.data->'info'->'players')->>'factions' as factions
#   FROM lor_game
#   WHERE lor_game.data->'info'->>'game_version' = 'live-green-3-13-42'
# ) as player
# GROUP BY deck_code, factions
# HAVING COUNT(*) > 10
# ORDER BY games DESC
# ```
# 
# Result:
# 
# | Deck code | Factions | Games | Wins |
# | --- | --- | --- | --- |
# | `CICQCAQDAMAQKBQBAEDA(...)` |	["faction_Bilgewater_Name", "faction_Noxus_Name"]	| 39880 |	24067 |
# | `CMCQCAQAAIAQIAADAECA(...)` |	["faction_Demacia_Name", "faction_Shurima_Name"] | 24118 | 12756 |
# | `CUFACAIEGYAQEBR4AEBQ(...)` |	["faction_Jhin_Name", "faction_Noxus_Name"]	| 16387 |	9315 |
# | `CMBQCAQAAIBAIB3HQIAQ(...)` |	["faction_Demacia_Name", "faction_Shurima_Name"]	|16153|	9146|
# | ...  | ... | ... | ... |
# 

# In[1]:


# Loading our env variables before we load our library
import dotenv

dotenv.load_dotenv(verbose=True, override=True)

# We checked for the latest patch value by looking at the most recent games
latest_version = "live-green-3-13-42"

# Connecting to the database
from neotokyo import db

session = db.connection.ghost_session_maker.session_maker()

# ORM
import sqlalchemy
from sqlalchemy.dialects import postgresql

# Defining our subquery, already filtered on the right game version
# Tbh the postgres JSONB syntax in SQLAlchemy is pretty disgusting
player_table = (
    sqlalchemy.select(
        sqlalchemy.func.jsonb_array_elements(
            db.models.LorGame.data["info"]["players"],
            type_=postgresql.JSONB,
        )["deck_code"].astext.label("deck_code"),
        sqlalchemy.func.jsonb_array_elements(
            db.models.LorGame.data["info"]["players"],
            type_=postgresql.JSONB,
        )["factions"].astext.label("factions"),
        sqlalchemy.func.jsonb_array_elements(
            db.models.LorGame.data["info"]["players"],
            type_=postgresql.JSONB,
        )["win"].astext.label("win"),
    )
    # We put our patch limit here so the subquery return is smaller
    .where(
        db.models.LorGame.data["info"]["game_version"].astext == latest_version,
    )
    .subquery()
)

games_count = sqlalchemy.func.count().label("games_count")
wins = sqlalchemy.func.count(
    sqlalchemy.case(
        (player_table.c.win == "true", 1),
    )
).label("wins")

# The disgusting player_table code lets us write a pretty clean and readable query at least!
query = (
    sqlalchemy.select(
        player_table.c.deck_code,
        player_table.c.factions,
        games_count,
        wins,
    )
    .order_by(games_count.desc())
    .group_by(
        player_table.c.deck_code,
        player_table.c.factions,
    )
    .having(games_count > 10)
)

# We get the results as a list
latest_patch_decks = session.execute(query).all()

print(f"Games found: {sum(dd.games_count for dd in latest_patch_decks):,}")


# 
# ### Deck codes to deck lists
# 
# Riot gives us [deck codes](https://github.com/RiotGames/LoRDeckCodes), but we want a list of cards to easily compute the distance. *Technically* one could implement the algorithm in pure SQL, but it's quite a pain.
# 
# We will instead use [lor-deckcodes](https://github.com/Rafalonso/LoRDeckCodesPython) to transform deck codes into a list of card codes and counts, and will then transform card cards into card names using our own database.
# 
# To store decklists in an easy to compare format we will use a **set** of 40 strings with card names postfixed by their occurence number:
# ```
# {
#   Veigar-1,
#   Veigar-2,
#   Veigar-3,
#   Senna-1,
#   ...
# }
# ```

# In[2]:


# Defining constants
DECK_SIZE = 40

# Adding a small utility to compute card names
card_cache = {}


def get_card_name(code: str) -> str:
    if code not in card_cache:
        card_cache[code] = session.get(db.models.LorCard, code).data["name"]

    return card_cache[code]


from typing import Set


# A small function to have more readable card lists
#   We don't do it based on deck codes/decklists because we want to use it with archetypes later
def cards_table(cards: Set[str]) -> str:
    """Beautiful output of cards"""
    import tabulate

    # We could do all that with complex list comprehensions but the gain in performance is not worth the loss in readability
    tabulate_input = []
    current_row = []
    added_cards = set()

    for card in sorted(
        cards,
        # The last character is the # of copies and we want to go in descending order
        key=lambda x: x[-1],
        reverse=True,
    ):
        card_name = card[:-2]

        # If we already added the card we continue
        if card_name in added_cards:
            continue

        added_cards.add(card_name)
        current_row.append(f"{card[-1]}x {card_name}")

        # We put only 4 cards per row
        if len(current_row) == 4:
            tabulate_input.append(current_row)
            current_row = []

    if current_row:
        tabulate_input.append(current_row)

    return tabulate.tabulate(tabulate_input, tablefmt="html")


# Making a dataclass to hold our information
from dataclasses import dataclass

# Utilities for outputting HTML
from IPython.display import HTML, display

# A dataclass automatically creates its own __init__ functions from type hints which is nice
@dataclass
class DeckData:
    deck_code: str

    factions: str
    cards: Set[str]

    games_count: int
    wins: int

    @property
    def winrate(self):
        return self.wins / self.games_count

    def display(self):
        display(
            HTML(
                f"""<h3>{self.deck_code}</b></h2>
<ul><li>Games: {self.games_count:,}</li>
<li>Winrate: {self.winrate*100:.2f}%</li>
<li>Factions: {self.factions}</li>
<li>Decklist: {cards_table(self.cards)}</li>"""
            )
        )


import lor_deckcodes

decks_data = {}

for row in latest_patch_decks:
    deck = lor_deckcodes.LoRDeck.from_deckcode(row.deck_code)

    # We store decklist as a set of 40 unique strings as it lets use the intersection operator
    # I tried storing decklists as sets of unique integers but saw no significant performance improvement
    cards = set()
    for card in deck.cards:
        for i in range(card.count):
            cards.add(f"{get_card_name(card.card_code)}-{i+1}")

    # Making sure we do have 40 unique card strings in our set
    assert len(cards) == DECK_SIZE

    # Saving all the data we got for this specific deck code
    decks_data[row.deck_code] = DeckData(
        deck_code=row.deck_code,
        factions=row.factions,
        games_count=row.games_count,
        wins=row.wins,
        cards=cards,
    )


print(f"Decks found: {len(decks_data):,}")

first_deck_code = next(iter(decks_data))
decks_data[first_deck_code].display()

print("Raw cards data: ", decks_data[first_deck_code].cards)


# ## Implementing incremental constrained cluster growth
# 
# ### Basic idea
# 
# - Define the **distance** from a deck to a cluster
# - Iterate on decks in descending popularity (# games)
# - For each deck
#   - Create a cluster containing only this deck
#   - Add decks one by one by, selecting the one with shortest distance to the cluster each step
# - Add non-overlapping clusters in descending size
# - Re-start iteration with any remaining decks
# 
# The **archetype** will be the aggregate decklist as defined by [Frank Karsten's in this ChannelFireball article](https://strategy.channelfireball.com/all-strategy/mtg/channelmagic-articles/magic-math-a-new-way-to-determine-an-aggregate-deck-list-rg-dragons/).
# 
# #### Things that didn't work out
# 
# - With a direct implementation, computational time was through the roof at **~24h with ~20,000 decks**
#   - Complexity `O(n**3)` does that
# - Even with multiple optimisations and shortcuts the method was still way too heavy and took multiple hours for each iteration
# 
# - I tried an idea I called *fast cutoff*, which would directly select a cluster if it contained more than 1% of all decks
#   - It did heavily speed up the process at the cost of clustering quality
#   - I was able to *not* need it anymore once I fixed my code
# 
# ### Deck factions
# 
# The most important thing to add was "pre-clustering". `O(n**3)` complexity means that if we're able to split the data into 100 sets, complexity goes down by 1,000,000.
# 
# And there are 100 obvious sets for our data: the deck's factions. Those are similar to deck colors in Magic or hero in Hearthstone.
# 
# Forcing all decks in an archetypes to be the same factions does lose some granularity for decks that just splash 3/6 cards in a different faction, but it's actually something we *want*. The end goal is identifying success of different strategies, and changing a splash in a deck is a new strategy.
# 
# The simplification also allowed me to drop the fast cutoff idea as I was working with much smaller lists of decks to cluster at each step.

# In[3]:


from collections import defaultdict

# Creating faction groups
# We use lists and not sets because we want to keep the decks ordered by count
factions_decks = defaultdict(list)

for deck_code in decks_data:
    factions_decks[decks_data[deck_code].factions].append(deck_code)

print(f"Found {len(factions_decks):,} different factions")

max_faction = max(factions_decks, key=lambda x: len(factions_decks[x]))
print(f"The faction with the most decks is", max_faction)


# ### Distance and clusters
# 
# #### Distance between two decks
# 
# Distance is calculated through the intersection operator for sets applied on the set of cards in the deck: `&`.
# 
# This works as each copy (1-2-3) is defined as a unique string in our decklists.
# 
# #### Distance from a deck to a cluster
# 
# The distance from a deck to a cluster is 0 if adding the new deck does not change the intersection of existing decks in the cluster. If it requires removing a card from the intersection to add the new deck, it's 1, and so on and so forth.
# 
# I initially implemented it wrongly, which cost me a lot of time.
# 
# The right way to calculate the distance from a deck to a cluster is to use the cluster's intersection and compare it to the decklist.
# 
# #### Implementation
# 
# What really matters to us is the distance of a deck to a cluster, so it's even easier to implement all those as part of a `Cluster` class.
# 
# While we're at it we implement the aggregate decklist code in that class as well as some basic stats handling and a beautiful display!

# In[4]:


from abc import abstractmethod
from collections import Counter
from typing import Optional

type_cache = {}


def get_card_type(name: str) -> str:
    if name not in type_cache:
        card = (
            session.query(db.models.LorCard)
            .filter(db.models.LorCard.data["name"].astext == name)
            .first()
        )
        type_cache[name] = card.data["supertype"]

    return type_cache[name]


# A class we'll use to compute cluster stats and display them
class ClusterStats:
    def __init__(self, cluster) -> None:
        self.cluster = cluster

        cards_count = Counter()

        self.wins = 0
        self.games_count = 0

        for deck_code in self.cluster.decks:
            self.games_count += decks_data[deck_code].games_count
            self.wins += decks_data[deck_code].wins
            self.factions = decks_data[deck_code].factions

            for card in decks_data[deck_code].cards:
                # Instead of just using 1, we use the decklists' wins
                #   This makes it so not only more popular versions have more weight, but successful ones do too
                cards_count[card] += decks_data[deck_code].wins

        self.aggregated_decklist = [c for c, count in cards_count.most_common(40)]

        champions = set(
            c[:-2]
            for c in self.aggregated_decklist
            if get_card_type(c[:-2]) == "Champion"
        )

        self.title = f"""{" ".join(champions)} - {
            " ".join(n[9:-6] for n in self.factions.replace(" ", "")[1:-1].split(","))
        }"""

    @property
    def winrate(self):
        return self.wins / self.games_count

    def display(self):
        display(
            HTML(
                f"""<h3>{self.title}</h3>
    <ul>
    <li><b>{self.winrate*100:.2f}% winrate</b></li>
    <li>{self.games_count:,} games</li>
    <li>{len(self.cluster.decks)} decklists</li>
    <li>Aggregated decklist: {cards_table(self.aggregated_decklist)}</li></ul>"""
            )
        )


class Cluster:
    def __init__(self, center: str) -> None:
        self.decks = [center]

    def __contains__(self, item) -> bool:
        return True if item in self.decks else False

    def __len__(self) -> int:
        return len(self.decks)

    @abstractmethod
    def distance(self, deck_code: str) -> int:
        ...

    @abstractmethod
    def can_be_added_to_cluster(self, distance: int) -> Optional[bool]:
        # TODO Check if we actually need that
        # We will use a trilean here
        #   True -> can be added
        #   False -> cannot be added yet
        #   None -> will never be able to be added (useful for some distances)

        # We use the distance as argument so we don't compute it twice but to allow for different rules
        ...

    @abstractmethod
    def add(self, deck_code: str) -> None:
        ...

    def get_stats(self) -> ClusterStats:
        return ClusterStats(self)


# ### Centered clusters
# 
# Given a `center` deck and a list of `candidates`, we want to find the "best" cluster built around `center`.
# 
# To do that, we add decks one by one, taking the *closest* one to the cluster at each step.
# 
# There are a few possible optimisations:
# - If a deck has a distance 0 to the cluster, we should be able to add it instantly
#     - Distance 0 should mean adding it doesn't change our cluster
# <!-- TODO CHECK 
# - Each deck whose addition would force the cluster's intersection to go below the number of `COMMON_CARDS` with the cluster can be removed directly
#     - This allows us to remove almost all decks on the first pass and then only add meaningful ones in order -->

# In[5]:


import copy
from typing import List
import time


def get_centered_cluster(
    center: str,
    candidates: List[str],
    cluster_class: Cluster,
) -> Cluster:

    # We start the cluster with the center
    cluster = cluster_class(center)

    # We remove it from the candidates
    candidates.remove(center)

    # We iterate until we aren't able to add an eligible deck or we've added them all
    while len(candidates) > 0:

        # This is the maximum value (fully disjointed decks)
        minimum_distance = float("inf")
        minimum_deck = None

        # We iterate on possible members
        # We copy the list because we want to be able to remove candidates during iteration
        for candidate in list(candidates):

            cluster_distance = cluster.distance(candidate)
            can_be_added = cluster.can_be_added_to_cluster(cluster_distance)

            # We check if the deck can be added to our cluster first
            if can_be_added is None:
                # We use a trilean to speed up the process with some algorithms
                candidates.remove(candidate)

            elif can_be_added is False:
                pass

            elif can_be_added is True:
                # If distance = 0 we can add the deck directly (happens for common cards clustering)
                if cluster_distance == 0:
                    cluster.add(candidate)
                    candidates.remove(candidate)
                    continue

                # We check if we found a new closest candidate and save it if that's the case
                if cluster_distance < minimum_distance:
                    minimum_distance = cluster_distance
                    minimum_deck = candidate

        # One step of iterations on candidates is over

        # If we didn't find a new minimum deck, we stop
        if minimum_deck is None:
            break

        # Adding the deck we found to our cluster
        cluster.add(minimum_deck)

        # We remove the deck from the remaining decks and continue iterating
        candidates.remove(minimum_deck)

    return cluster


# ### Getting all clusters
# 
# Then, we make a function for getting all clusters for a list of deck codes. This one's pretty simple.

# In[6]:


from typing import List


def get_all_clusters(deck_codes: List[str], cluster_class: Cluster) -> List[Cluster]:
    """Gets all clusters centered on each deck code

    Args:
        deck_codes (List[str]): a list of deck codes

    Returns:
        List[Cluster]: all clusters found centered on each deck code
    """
    clusters = []

    for center in deck_codes:
        # We copy the list of deck codes because we change it in our code above
        candidates = list(deck_codes)

        # We get the biggest cluster centered on deck
        clusters.append(get_centered_cluster(center, candidates, cluster_class))

    return clusters


# ### Clustering a list of decks
# 
# We now have all the necessary building blocks to make our last function. One that takes a list of deck codes and returns clusters containing all decks.
# 
# Pseudocode:
# - Call `get_all_clusters` to get all clusters centered on each remaining deck code
# - Order them by size
# - Add them in descending size order as long as they don't contain any deck that's already in our result
#     - The biggest one will always get added
#     - Smaller ones can get added directly if they have no overlap with the big clusters found in that step
# - Restart the process until all decks have been assigned to a cluster

# In[7]:


def get_best_clusters(deck_codes: List[str], cluster_class: Cluster) -> List[Cluster]:
    """Gets the best clusters for the list of deck codes

    Args:
        deck_codes (List[str]): a list of deck codes

    Returns:
        List[Cluster]: the best clusters found
    """
    clusters = []
    remaining_decks = deck_codes

    def clusters_contains_deck(clusters: List[Cluster], deck) -> bool:
        # Return True if the deck is in any of the clusters already found
        return any(deck in c for c in clusters)

    while len(remaining_decks) > 0:
        possible_clusters = get_all_clusters(remaining_decks, cluster_class)

        for possible_cluster in sorted(
            possible_clusters, key=lambda x: len(x), reverse=True
        ):
            # If no other cluster already contains any of the decks in the current candidate cluster, we add it
            # This means we will always add the biggest cluster found at that step
            if all(not clusters_contains_deck(clusters, d) for d in possible_cluster.decks):
                clusters.append(possible_cluster)

            # Else we pass to the next possible cluster
            else:
                continue

        # We update our remaining decks
        remaining_decks = [
            d for d in deck_codes if not clusters_contains_deck(clusters, d)
        ]

    return clusters


# ## Clustering based on common cards
# 
# - All decks in an archetype must share `ARCHETYPE_SIZE` cards
# - Any deck whose addition would make the cluster intersection go below `ARCHETYPE_SIZE` can directly be eliminated
#     - Adding more decks will make the cluster *more* stringent with future additions

# In[8]:


ARCHETYPE_SIZE = DECK_SIZE - 10

class CommonCardsCluster(Cluster):
    def __init__(self, center: str) -> None:
        super().__init__(center)

        # Saving the intersection of the decklists in our cluster will help speed up the process
        self.intersection = decks_data[center].cards

        self.archetype_size = ARCHETYPE_SIZE

    @staticmethod
    def deck_to_deck_distance(dc_1: str, dc_2: str):
        # A small class method for validation
        return DECK_SIZE - len(
            # & is the intersection operator for sets
            decks_data[dc_1].cards
            & decks_data[dc_2].cards
        )

    def distance(self, deck_code: str) -> int:
        # If the cluster_intersection is fully contained in the decks_data cards, cluster_intersection = cluster + deck intersetion and len = 0
        # This will always be >= 0 because at most there's full overlap between a deck and a cluster's intersection
        return len(self.intersection) - len(
            # & is the intersection operator for sets
            self.intersection
            & decks_data[deck_code].cards
        )

    def can_be_added_to_cluster(self, distance: int) -> Optional[bool]:
        # If adding the new deck would make the intersection go over the archetype size, it will never be able to be added
        # For example if we currently have an intersection of 30 and an archetype size of 28, the max distance to add is 2
        if distance > len(self.intersection) - self.archetype_size:
            return None

        else:
            return True

    def add(self, deck_code: str) -> None:
        self.decks.append(deck_code)
        # & is the intersection operator for sets
        self.intersection = self.intersection & decks_data[deck_code].cards


# In[9]:


for deck_code in decks_data:
    # A deck code has 100% overlap with itself
    assert CommonCardsCluster.deck_to_deck_distance(deck_code, deck_code) == 0

    if deck_code != first_deck_code:
        # deck-to-deck distance is always > 0 as they're distinct and <= 40 as that's the maximum difference
        assert (
            0
            < CommonCardsCluster.deck_to_deck_distance(deck_code, first_deck_code)
            <= 40
        )

        # In this specific case, the distance to the cluster is the same as the distance to the deck:
        #   it's the number of non-overlapping cards
        cluster = CommonCardsCluster(first_deck_code)

        assert cluster.distance(deck_code) == CommonCardsCluster.deck_to_deck_distance(
            deck_code, first_deck_code
        )

# Validation of the centered clusters code
for deck in factions_decks[max_faction][:200]:

    # Only checking out of 200 decks for speed
    cluster = get_centered_cluster(
        deck,
        factions_decks[max_faction][:200],
        CommonCardsCluster,
    )

    # We check the number of cards common to all decks in the cluster
    if len(cluster.decks) > 1:
        # If have more than one deck, their intersection is at most 39 cards
        assert 40 > len(cluster.intersection) >= ARCHETYPE_SIZE
    else:
        # A few decks simple have no good neigbors, we check the distance is > DECK_SIZE - ARCHETYPE_SIZE
        assert min(cluster.distance(d) for d in factions_decks[max_faction][:200] if d != deck) > DECK_SIZE - ARCHETYPE_SIZE

# Validation of the best clusters code
clusters = get_best_clusters(factions_decks[max_faction][:200], cluster_class=CommonCardsCluster)

# We clustered 200 decks, the sum of clusters lengths should be 200
assert sum(len(c) for c in clusters) == 200

# Checking we have the right intersection sizes
for cluster in clusters:
    assert 40 >= len(cluster.intersection) >= ARCHETYPE_SIZE


# ### Putting it all together
# 
# #### Parameter selection
# 
# Selecting the right `ARCHETYPE_SIZE` is crucial so I experimented with a few different values. Keep in mind we have ~30,000 decklists.
# 
# | ARCHETYPE_SIZE | ARCHETYPES | AVG DECK/ARCHETYPE FOR TOP 100 |
# | --- | --- | --- | 
# | 30 | 10132 | 53 |
# | 28 | 8847 | 65 |
# | 25 | 7032 | 80 |
# 
# `ARCHETYPE_SIZE=28` looks like a good spot for archetype size and is coherent with the intuition of what defines an archetype. It allows for 12 cards to be different between decklists, which is 4 individual playsets of cards.
# 
# At the same time, the most popular archetype (Senna Veigar) contains over **500 different decks** which is starting to obscure a lot of individual card choices which may be meaningful.
# 
# A dynamic `ARCHETYPE_SIZE` might be what's needed, in particular for decks which have a lot of "flex" slots. Smaller changes in those popular decks could create new archetypes, and fringe decks could get grouped more easily to allow for easier analysis. This might be something I explore in the future.
# 
# #### Analysing the results
# 
# And finally we get to the fun part, running it and finding out what's the best deck in Legends of Runeterra right now!
# 
# Or so I thought. Let's take a look at the result.

# In[10]:


# This will be a list of lists containing deck codes
common_cards_cluster = []

# Progress visualization
from tqdm.notebook import tqdm

# Running the clustering process for all regions takes a few minutes
# It could be heavily optimized but it's good enough for now
for faction in tqdm(factions_decks):
    best_clusters = get_best_clusters(factions_decks[faction], CommonCardsCluster)
    common_cards_cluster.extend(best_clusters)


# In[11]:


# We'll take a look at the 100 archetypes with the most games
for cluster in sorted(common_cards_cluster, key=lambda x: len(x), reverse=True)[:100]:
    stats = cluster.get_stats()

    if "Miss Fortune" in stats.title and "Twisted Fate" in stats.title:
        stats.display()


# As we can see, we have 3 archetypes that are... Pretty much the same MF-TF aggro deck. The differences in their aggregate decklists are minimal, and they should not be 3 different archetypes, or split differently at least.
# 
# I think this is due to the fact that players will try pretty much *any* change to a decklist, which means each individual card will get cut from the decklist at some point. Archetypes aren't really defined by cards they *all* have in common, but more by *how many* cards they have in common.
# 
# So it's time to implement our second distance!

# ## Clustering based on cards differences
# 
# Let's take the opposite approach:
# 
# - The distance of a deck to a cluster is the **maximum** number of different cards it has with a deck in the cluster
# - We will add new decks by minimizing this maximum distance
# - We will set a limit on the maximum distance between two decks in an archetype
# 
# The goal is to add decks that differ slightly from eachother, whichever cards the players decide to change.
# 
# Even though the number seems high at `MAX_DIFFERENCE=15`, it's the *maximum* difference between two arbitrary decks in the cluster. As the clusters are formed iteratively, similar decks will get grouped together early and hopefuly it won't catch too many "parallel" archetypes.

# In[12]:


# This will be the maximum number of different cards 2 different decks can have while in the same cluster
MAX_DIFFERENCE = 15


# Global distance cache
decks_distance_cache = defaultdict(dict)


def deck_to_deck_distance(dc_1: str, dc_2: str):
    # This time we will use this distance heavily and add a distance cache

    # We sort the decks
    d1, d2 = sorted((dc_1, dc_2))

    if d2 not in decks_distance_cache[d1]:
        decks_distance_cache[d1][d2] = DECK_SIZE - len(
            # & is the intersection operator for sets
            decks_data[d1].cards
            & decks_data[d2].cards
        )

    return decks_distance_cache[d1][d2]


class DifferenceBasedCluster(Cluster):
    def __init__(self, center: str) -> None:
        super().__init__(center)

        self.max_difference = MAX_DIFFERENCE

        # Internal cluster distance cache to speed up max search
        # Each deck will point to its maximum distance to the cluster
        # Which means when iterating a deck, we only need to check what's biggest between the max distance in the cache and the one with the last deck added
        self.cluster_distance_cache = defaultdict(lambda: 0)

    def distance(self, deck_code: str) -> int:
        # We could do max(self.deck_to_deck_distance(d, deck_code) for d in self.decks)
        # But we want to speed things up and any deck with a distance > MAX_DIFFERENCE can be ruled out directly
        max_distance = max(self.cluster_distance_cache[deck_code], deck_to_deck_distance(deck_code, self.decks[-1]))

        # In this situation the deck we selected will be too far, we return the maximum value and we'll remove the deck
        if max_distance > self.max_difference:
            return float("inf")

        # Else we save the new value
        self.cluster_distance_cache[deck_code] = max_distance
        
        return max_distance

    def can_be_added_to_cluster(self, distance: int) -> Optional[bool]:
        # By now I realize this function was superfluous, and we could have relied on distance() returning float("inf") as our way to prune decks
        #   Refactoring notebooks is a huge pain though so I won't change it :D

        # If adding the new deck would make the intersection go over the archetype size, it will never be able to be added
        # For example if we currently have an intersection of 30 and an archetype size of 28, the max distance to add is 2
        if distance == float("inf"):
            return None

        else:
            return distance < self.max_difference

    def add(self, deck_code: str) -> None:
        self.decks.append(deck_code)


# In[13]:


for deck_code in decks_data:
    # A deck code has 100% overlap with itself
    assert deck_to_deck_distance(deck_code, deck_code) == 0

    if deck_code != first_deck_code:
        # deck-to-deck distance is always > 0 as they're distinct and <= 40 as that's the maximum difference
        assert 0 < deck_to_deck_distance(deck_code, first_deck_code) <= 40

        # In this specific case, the distance to the cluster is the same as the distance to the deck:
        #   it's the number of non-overlapping cards
        cluster = DifferenceBasedCluster(first_deck_code)

        # Our cluster distance returns float("inf") if deck is too far, so we need to check >= here
        assert cluster.distance(deck_code) >= deck_to_deck_distance(
            deck_code, first_deck_code
        )

# Validation of the centered clusters code
for deck in factions_decks[max_faction][:200]:

    # Only checking out of 200 decks for speed
    cluster = get_centered_cluster(
        deck,
        factions_decks[max_faction][:200],
        DifferenceBasedCluster,
    )

    assert len(cluster.decks)

# Validation of the best clusters code
clusters = get_best_clusters(
    factions_decks[max_faction][:200],
    cluster_class=DifferenceBasedCluster,
)

# We clustered 200 decks, the sum of clusters lengths should be 200
assert sum(len(c) for c in clusters) == 200


# ### Checking results
# 

# In[14]:


# This will be a list of lists containing deck codes
difference_based_clusters = []

# Progress visualization
from tqdm.notebook import tqdm

# Running the clustering process for all regions is ~1 hour with that algorithm
# It could be heavily optimized but let's say it's ok for now
for faction in tqdm(factions_decks):
    best_clusters = get_best_clusters(factions_decks[faction], DifferenceBasedCluster)
    difference_based_clusters.extend(best_clusters)


# In[15]:


# We'll take a look at the 1000 archetypes with the most games
for cluster in sorted(difference_based_clusters, key=lambda x: len(x), reverse=True)[:100]:
    stats = cluster.get_stats()

    if stats.title.startswith("Miss Fortune Twisted Fate"):
        stats.display()


# Looks better! We only have a single pirates aggro list that properly catches the decklists from the 3 previous ones we had.
# 
# So after all this... Let's take a look at the best decks and call it a day :D

# In[27]:


# Let's take a look at the 100 archetypes with the most games and print the 10 highest winrates amongst tho
for cluster in sorted(
    sorted(difference_based_clusters, key=lambda x: len(x), reverse=True)[:100],
    key=lambda x: x.get_stats().winrate,
    reverse=True,
)[:10]:
    stats = cluster.get_stats()
    stats.display()


# # Conclusion
# 
# Because clustering is still excruciatingly slow, I'm not really satisfied with this first approach.
# 
# At the same time we can use heuristics for clustering. For Legends of Runeterra, this can simply be looking at champions and regions.
# 
# If you have any other idea for how to implement clustering for card games in an even more game-agnostic way, don't hestitate! I'll still be looking at the subject moving forward, even though this blogpost already took me much more time than expected as my first notebook-based blog post.
