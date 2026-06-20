from abc import ABC, abstractmethod

CATEGORIES = {
    "Trending Now": [
        ("The Last Voyage", "#8B0000"), ("Crimson Tide", "#1a5276"),
        ("Night Falls", "#4a235a"), ("Golden Hour", "#b7950b"),
        ("Echoes of Tomorrow", "#117a65"), ("Silver Lining", "#7d6608"),
        ("The Long Road", "#6c3483"), ("Starlight", "#1b4f72"),
        ("Midnight Rain", "#922b21"), ("Shadow Realm", "#0e6655"),
    ],
    "Popular Movies": [
        ("Midnight Express", "#922b21"), ("Ocean Deep", "#1a5276"),
        ("Desert Storm", "#b9770e"), ("Urban Legends", "#512e5f"),
        ("Hidden Depths", "#148f77"), ("Wildfire", "#a93226"),
        ("Paper Moon", "#7d3c98"), ("Open Skies", "#2e86c1"),
        ("Thunderstrike", "#7b241c"), ("Iron Will", "#1b4f72"),
    ],
    "Popular TV Series": [
        ("Crown & Glory", "#6c3483"), ("Shadow Unit", "#1b4f72"),
        ("Crystal Lake", "#0e6655"), ("Iron Circuit", "#7b241c"),
        ("Neon Nights", "#4a235a"), ("Sapphire Skies", "#154360"),
        ("Thunder Alley", "#935116"), ("Winter Frost", "#1a5276"),
        ("Ember Falls", "#922b21"), ("Ghost Protocol", "#4a235a"),
    ],
    "Action & Adventure": [
        ("Thunderstrike", "#922b21"), ("Force Majeure", "#1b4332"),
        ("Bulletproof", "#4a235a"), ("Rapid Fire", "#b9770e"),
        ("Impact Zone", "#7b241c"), ("Renegade", "#1a5276"),
        ("Lock & Load", "#935116"), ("Blitz", "#0e6655"),
    ],
    "Comedy": [
        ("Laugh Track", "#7d6608"), ("Funny Business", "#117a65"),
        ("Comedy Gold", "#6c3483"), ("Stand Up", "#b7950b"),
        ("Hilarious", "#1a5276"), ("Comic Relief", "#935116"),
        ("Joke's On You", "#922b21"), ("Lighthearted", "#148f77"),
    ],
    "Drama": [
        ("Broken Pieces", "#6c3483"), ("Silent Echo", "#1a5276"),
        ("The Divide", "#7b241c"), ("Fading Light", "#b9770e"),
        ("Tender Is the Night", "#117a65"), ("Crossroads", "#935116"),
        ("Aftermath", "#4a235a"), ("Memoir", "#922b21"),
    ],
    "Documentaries": [
        ("Blue Planet", "#1a5276"), ("Nature's Call", "#0e6655"),
        ("Ancient Worlds", "#6c3483"), ("Deep Dive", "#148f77"),
        ("Unsolved", "#4a235a"), ("Through the Lens", "#7d6608"),
        ("True Stories", "#922b21"), ("Horizons", "#1b4f72"),
    ],
}

class Content(ABC):
    def __init__(self, title, color, year, description, rating):
        self._title = title
        self._color = color
        self._year = year
        self._description = description
        self._rating = rating

    def get_title(self):
        return self._title

    def get_color(self):
        return self._color

    def get_year(self):
        return self._year

    def get_description(self):
        return self._description

    def get_rating(self):
        return self._rating

    @abstractmethod
    def get_type_label(self):
        pass

    @abstractmethod
    def get_info_lines(self):
        pass

    def __repr__(self):
        return f"{self._title} ({self.get_type_label()}, {self._year})"


class Movie(Content):
    def __init__(self, title, color, year, description, rating, duration, director):
        super().__init__(title, color, year, description, rating)
        self._duration = duration
        self._director = director

    def get_type_label(self):
        return "Movie"

    def get_info_lines(self):
        return [
            f"Director: {self._director}",
            f"Duration: {self._duration} min",
            f"Rating: {self._rating}/10",
        ]


class TVShow(Content):
    def __init__(self, title, color, year, description, rating, seasons, episodes_per_season):
        super().__init__(title, color, year, description, rating)
        self._seasons = seasons
        self._episodes_per_season = episodes_per_season

    def get_type_label(self):
        return "TV Series"

    def get_info_lines(self):
        return [
            f"Seasons: {self._seasons}",
            f"Episodes: {self._seasons * self._episodes_per_season}",
            f"Rating: {self._rating}/10",
        ]