"""
CSC111 Project 2: Wrap Mapped, Unpacked
Authors: Colleen Chang, Richard Lin, Roy Liu, Mina (Chieh-Yi) Wu

File Description
=============================================================================
This file contains necessary classes for the program.

"""
from __future__ import annotations
from typing import Any, Optional, Union
import python_ta


class Tree:
    """A recursive tree data structure.

          Representation Invariants:
                  - self._root is not None or self._subtrees == []
                  - all(not subtree.is_empty() for subtree in self._subtrees)
          """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """
        Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
        Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """
        Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def insert_sequence(self, items: list) -> None:
        """Inserts a sequence of items into this tree.

        (Definition from CSC111 Exercise 2)
        The inserted items form a chain of descendants, where:
        - items[0] is a child of this tree's root
        - items[1] is a child of items[0]
        - items[2] is a child of items[1]
        - etc.

        Preconditions:
            - not self.is_empty()
        """
        if items:
            in_subtrees = False
            for subtree in self._subtrees:
                if subtree._root == items[0] and not in_subtrees:
                    subtree.insert_sequence(items[1:])
                    in_subtrees = True

            if not in_subtrees:
                new_tree = Tree(items[0], [])
                new_tree.insert_sequence(items[1:])
                self._subtrees.append(new_tree)

    def navigate_sequence(self, items: list) -> Optional[Tree]:
        """Navigates and returns the tree that contains the last item in the given sequence of items
        Otherwise, return None if the sequence isn't in this tree.

        Note: The first item in "items" should be a child of this tree.
        """
        if len(items) == 0:
            return self
        elif items:
            for subtree in self._subtrees:
                if subtree._root == items[0]:
                    return subtree.navigate_sequence(items[1:])

        return None

    def get_all_countries_sequence(self) -> list[tuple[Tree, list[str]]]:
        """Returns a list of tuples for each country. Each tuple contains a subtree representing
        a country in this tree and a list of the sequence from a continent to the country.

        Mainly a helper for "region_personality" function.

        Precondtions:
            - self._root == 'World'
        """
        countries = []
        for continent in self._subtrees:
            for country in continent._subtrees:
                countries.append((country, [continent._root, country._root]))
        return countries

    def get_all_cities_sequence(self) -> list[tuple[Tree, list[str]]]:
        """Returns a list of tuples for each city. Each tuple contains a subtree representing
        a city in this tree and a list of the path from a continent to the city.

        Mainly a helper for "region_personality" function.

        Precondtions:
            - self._root == 'World'
        """
        cities = []
        for continent in self._subtrees:
            for country in continent._subtrees:
                for city in country._subtrees:
                    cities.append((city, [continent._root, country._root, city._root]))
        return cities

    def get_songs(self) -> set[Song]:
        """Returns a set of all songs/leaves found in this tree
        """
        if isinstance(self._root, Song):
            return {self._root}
        elif not self.is_empty():
            songs = set()
            for subtree in self._subtrees:
                songs = songs.union(subtree.get_songs())
            return songs
        return set()

    def get_all_song_titles(self) -> set[str]:
        """Returns all of the song titles in the tree
        """
        titles = set()
        songs = self.get_songs()
        for s in songs:
            titles.add(s.title)
        return titles

    def top_n(self, n: int, target: str) -> list[tuple]:
        """
        This function takes in the tree itself, an int representing the number of top songs to return,
        and a target representing whether you want to find top songs from the world, continent, country, or city.
        Returns a list of tuple with the top n songs, their artists, and stream. Returns [] if the target is not found.

        Representation Invariants:
            - n >= 1
        """
        if self._root == target:
            return self._search_songs(n, {}, {}, {})
        elif self._subtrees == []:
            return []
        else:
            for subtree in self._subtrees:
                top = subtree.top_n(n, target)
                if top != []:
                    return top

            return []

    def _search_songs(self, n: int, songs: dict, s_and_artist: dict,
                      s_and_stream: dict) -> list[tuple]:
        """
        This is a helper function for top_n, it returns the name, artist,
        and streams of the top n songs in a list of tuples.
        """

        if isinstance(self._root, Song):
            if self._root.title in songs:
                songs[self._root.title] += 1
            else:
                songs[self._root.title] = 1

            s_and_artist[self._root.title] = self._root.artist
            s_and_stream[self._root.title] = self._root.streams
            return []

        else:
            for subtree in self._subtrees:
                subtree._search_songs(n, songs, s_and_artist, s_and_stream)

            songs = dict(sorted(songs.items(), key=lambda x: x[1], reverse=True))
            songs = list(songs)
            lst = []
            for i in range(n):
                if i >= len(songs):
                    return lst

                lst += [(songs[i], s_and_artist[songs[i]], s_and_stream[songs[i]])]

            return lst

    def common_artist(self, country1: str, country2: str) -> list[str]:
        """
        This function takes in two country names as inputs and compares the artists of the top songs
        from each country and outputs a list of the most commonly occurring artists between the two countries
        in descending order.

        """
        top_songs_1 = self.top_n(100, country1)
        top_songs_2 = self.top_n(100, country2)

        top_songs1_dict = {}
        for song1 in top_songs_1:
            if song1[1] in top_songs1_dict:
                top_songs1_dict[song1[1]] += 1
            else:
                top_songs1_dict[song1[1]] = 1

        top_songs2_dict = {}
        for song2 in top_songs_2:
            if song2[1] in top_songs2_dict:
                top_songs2_dict[song2[1]] += 1
            else:
                top_songs2_dict[song2[1]] = 1

        common_artist = {}
        for artist in top_songs1_dict:
            if artist in top_songs2_dict:
                if top_songs1_dict[artist] <= top_songs2_dict[artist]:
                    common_artist[artist] = top_songs1_dict[artist]

        common_artist = dict(
            sorted(common_artist.items(), key=lambda x: x[1], reverse=True))
        common_artist = list(common_artist)
        return common_artist

    def common_song(self, country1: str, country2: str) -> list[str]:
        """
        This function takes in two country names as inputs and compares the top songs
        from both and outputs a list ofthe most commonly occurring songs between them in descending order.
        """
        top_songs_1 = self.top_n(100, country1)
        top_songs_2 = self.top_n(100, country2)

        top_songs1_dict = {}
        for song1 in top_songs_1:
            if song1[0] in top_songs1_dict:
                top_songs1_dict[song1[0]] += 1
            else:
                top_songs1_dict[song1[0]] = 1

        top_songs2_dict = {}
        for song2 in top_songs_2:
            if song2[0] in top_songs2_dict:
                top_songs2_dict[song2[0]] += 1
            else:
                top_songs2_dict[song2[0]] = 1

        common_song = {}
        for song in top_songs1_dict:
            if song in top_songs2_dict:
                if top_songs1_dict[song] <= top_songs2_dict[song]:
                    common_song[song] = top_songs1_dict[song]

        common_song = dict(
            sorted(common_song.items(), key=lambda x: x[1], reverse=True))
        common_song = list(common_song)
        return common_song

    def most_common_artist_country(self, country1: str) -> str:
        """
        This function takes in a country name as an input and compares the artists of the top songs from
        this country to all other countries in the tree and outputs a list of the most common country

        Preconditions:
            - self._root == 'World'
        """
        countries = set()
        for continent in self._subtrees:
            for country in continent._subtrees:
                if country._root != country1:
                    countries.add(country._root)

        country_top_artist = self.common_song_artist_helper(country1, 'artist')
        most_similar = {}

        for country in countries:
            temp_country_list = self.common_song_artist_helper(country, 'artist')
            for artist in temp_country_list:
                if artist in country_top_artist and country in most_similar:
                    most_similar[country] += 1
                elif artist in country_top_artist:
                    most_similar[country] = 1

        most_similar = dict(
            sorted(most_similar.items(), key=lambda x: x[1], reverse=True))
        most_similar = list(most_similar)
        most_similar = most_similar[0]

        return most_similar

    def most_common_song_country(self, country1: str) -> str:
        """
        This function takes in a country name as an input and compares the top songs from
        this country to the top songs in all other countries in the tree and outputs a list
        of the most common country

        Preconditions:
            - self._root == 'World'
        """

        countries = set()
        for continent in self._subtrees:
            for country in continent._subtrees:
                if country._root != country1:
                    countries.add(country._root)

        country_top_songs = self.common_song_artist_helper(country1, 'song')
        most_similar = {}

        for country in countries:
            temp_country_list = self.common_song_artist_helper(country, 'song')
            for song in temp_country_list:
                if song in country_top_songs and country in most_similar:
                    most_similar[country] += 1
                elif song in country_top_songs:
                    most_similar[country] = 1

        most_similar = dict(
            sorted(most_similar.items(), key=lambda x: x[1], reverse=True))
        most_similar = list(most_similar)
        most_similar = most_similar[0]

        return most_similar

    def common_song_artist_helper(self, country: str, c_type: str) -> list[str]:
        """
              Returns the top 5 artists/songs in a particular country

              Representation Invariants:
                  - c_type in {'artist', 'song'}

              """
        top_songs = self.top_n(5, country)
        top = []

        if c_type == 'artist':
            for artist in top_songs:
                top.append(artist[1])
        else:
            for song in top_songs:
                top.append(song[0])

        return top

    def get_comparison_score(self, songs: list[str], ranked: bool = False) -> float:
        """Computes a comparison score of this region to the provided songs list.

        The comparison score is calculated on the following specifications:
        - Not ranked:
            sim_score = total number of songs in both "songs" and this region / total number of songs in this region
        - ranked:
            sim_score = sum(ranked_scores) / total number of songs in this region

            where each score in ranked_score is calculated as follows:
                Let song be a song in this region's total set of songs
                if song is not in "songs" list: score = 0
                else: score = 1 - (abs(rank_of_song_in_songs - rank_of_song_in_city) / 5)

        The final score is rounded to the 5th decimal place.

        Preconditions:
            - self is a tree representing a region
            - isinstance(self._root, str)
            - 1 <= len(songs) <= 5
        """
        total_score = 0
        num_songs = 0

        # initializes a dictionary to hold the rankings of the user's inputs
        ranked_dict = {}
        if ranked:
            for i in range(len(songs)):
                ranked_dict[songs[i]] = i + 1

        region_songs = self.get_songs()
        for song in region_songs:
            if song.title in songs and ranked:
                total_score += 1 - (abs(ranked_dict[song.title] - song.rank) / 5)
            elif song.title in songs:
                total_score += 1
            num_songs += 1

        if num_songs == 0:
            return 0.0
        else:
            return round(total_score / num_songs, 5)

    def region_personality(self, n: int, songs: list[str],
                           region_range: str, ranked: bool = False) -> list[tuple[float, list[str]]]:
        """Returns a list with n tuples containing regions who have the highest similarity score to the given songs.
        In each tuple, the first element is the score, and the second element contains a list
        of the sequence from a continent to the region being tested.

        Preconditions:
            - n >= 1
            - all(song in self.get_all_song_titles() for song in songs)
            - region_range in {'continent', 'country', 'city'}
            - self._root == "World"
            - 1 <= len(songs) <= 5
        """
        scores = []

        if region_range == 'continent':
            for continent in self._subtrees:
                com_score = continent.get_comparison_score(songs, ranked)
                sequence = [continent._root]
                scores.append((com_score, sequence))
        elif region_range == 'country':
            countries = self.get_all_countries_sequence()
            for country in countries:
                com_score = country[0].get_comparison_score(songs, ranked)
                sequence = country[1]
                scores.append((com_score, sequence))
        else:
            cities = self.get_all_cities_sequence()
            for city in cities:
                if city[0]._root != '0':
                    com_score = city[0].get_comparison_score(songs, ranked)
                    sequence = city[1]
                    scores.append((com_score, sequence))

        scores.sort(reverse=True)
        return scores[:min(len(scores), n)]

    def recommend_songs(self, lim: tuple[int, int], songs: list[str],
                        region_range: str, ranked: bool = False) -> list[Song]:
        """Returns a max of lim[0] new song recommendations from the top lim[1] regions with the highest
        similarity score with the songs list.

        Preconditions:
            - self._root == 'World'
            - 1 <= len(songs) <= 5
        """
        recommendations = []
        recommended_songs = set()
        scores = self.region_personality(lim[1], songs, region_range, ranked)

        for score in scores:
            sequence = score[1]
            region = self.navigate_sequence(sequence)
            region_songs = region.get_songs()

            # finds new songs in top scored regions for recommendations
            for r_song in region_songs:
                if r_song.title not in songs and r_song.title not in recommended_songs:
                    recommendations.append(r_song)
                    recommended_songs.add(r_song.title)

        return recommendations[:min(lim[0], len(recommendations))]

    def get_region_streams(self, kind: str) -> dict[str, int] | dict[tuple, int]:
        """
        Returns dictionary mapping parts of a region with the total number of streams from their top 5 songs.

        Preconditions:
            - kind in {"continent", "country", "city"}
            - self.is_empty == False
        """

        def get_stream_stat(tree: Tree, target: str) -> int:
            """
            Returns the total stream count from the top 5 songs OVERALL from a tree's subroots since stream numbers are
            taken from a country's total streams for one song (not by specific cities/states)

            Preconditions:
                - tree.is_empty == False
            """
            return sum([song[2] for song in tree.top_n(5, target)])

        # return roots of all subtrees listed in a given set
        if kind == "continent":
            continents = self.get_regions_as_subtrees("continent")
            return {continent._root: get_stream_stat(self, continent._root) for continent in continents}
        elif kind == "country":
            countries = self.get_regions_as_subtrees("country")
            return {curr_country._root: get_stream_stat(self, curr_country._root) for curr_country in countries}
        else:
            countries = self.get_regions_as_subtrees("country")

            tups = []
            for country in countries:
                for city in country._subtrees:
                    tups.append((city._root, country._root))

            return {tup: get_stream_stat(self, tup[0]) for tup in tups}

    def get_region_scores(self, songs: list[str], kind: str, ranked: bool = False) \
            -> dict[str, float] | dict[tuple, float]:
        """
        Returns dictionary mapping parts of a region with their comparison/similarity score based on the list of songs
        given.

        Preconditions:
            - kind in {"continent", "country", "city"}
            - self.is_empty == False
            - self is a tree representing a region
            - isinstance(self._root, str)
            - 1 <= len(songs) <= 5
        """
        if kind == "continent":
            continents = self.get_regions_as_subtrees("continent")
            return {continent._root: continent.get_comparison_score(songs, ranked) for continent in continents}
        elif kind == "country":
            countries = self.get_regions_as_subtrees("country")
            return {curr_country._root: curr_country.get_comparison_score(songs, ranked) for curr_country in countries}
        else:
            countries = self.get_regions_as_subtrees("country")

            tups = []
            for country in countries:
                for city in country._subtrees:
                    tups.append((city, city._root, country._root))

            return {(tup[1], tup[2]): tup[0].get_comparison_score(songs, ranked) for tup in tups}

    def get_region_top_songs(self, kind: str) -> dict[str, list[str]] | dict[tuple, list[str]]:
        """
        Returns dictionary mapping parts of a region with lists of their top 5 songs in descending order of
        number of streams.

        Preconditions:
                - tree.is_empty == False
        """

        def get_top_5(tree: Tree, target: str) -> list[str]:
            """
            Returns list of the NAMES of the top 5 songs in a specific region in descending order of number of
            streams.
            """
            return [song[0] for song in tree.top_n(5, target)]

        if kind == "continent":
            continents = self.get_regions_as_subtrees("continent")
            return {continent._root: get_top_5(self, continent._root) for continent in continents}
        elif kind == "country":
            countries = self.get_regions_as_subtrees("country")
            return {curr_country._root: get_top_5(self, curr_country._root) for curr_country in countries}
        else:
            countries = self.get_regions_as_subtrees("country")

            tups = []
            for country in countries:
                for city in country._subtrees:
                    tups.append((city._root, country._root))

            return {tup: get_top_5(self, tup[0]) for tup in tups}

    def get_regions_as_subtrees(self, kind: str) -> set[Tree]:
        """
        Helper that returns set of all different regions based on the kind specified.

        Preconditions:
            - kind in {"continent", "country", "city"}
            - self.is_empty == False
            - self._root == "World"
        """
        continents = set(self._subtrees)

        if kind == "continent":
            return continents
        else:
            countries = set()
            for continent in continents:
                for country in continent._subtrees:
                    countries.add(country)
        if kind == 'country':
            return countries
        else:
            cities = set()
            for country in countries:
                for city in country._subtrees:
                    cities.add(city)
            return cities


class Song:
    """A class storing metadata of a song.
    Instance Attributes:
      - title: the name of the song
      - artist: the name of the first artist
      - streams: the number of streams of the song
      - rank: The rank of the song in the city/country

    Representation Invariants:
        - self.streams >= 0
        - 1 <= self.rank <= 5
    """
    title: str
    artist: str
    streams: Union[int, str]
    rank: int

    def __init__(self, title: str, artist: str, streams: Union[int, str], rank: int) -> None:
        self.title = title
        self.artist = artist
        self.streams = streams
        self.rank = rank


if __name__ == "__main__":
    python_ta.check_all(config={
        'max-line-length': 120
    })
