from abc import ABC, abstractmethod


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


CATEGORIES = {
    "Trending Now": [
        Movie("The Last Voyage", "#8B0000", 2023, "Placeholder description.", 8.2, 118, "James Carter"),
        Movie("Crimson Tide", "#1a5276", 2021, "Placeholder description.", 7.5, 124, "Sarah Mitchell"),
        Movie("Night Falls", "#4a235a", 2022, "Placeholder description.", 8.0, 110, "David Ross"),
        Movie("Golden Hour", "#b7950b", 2020, "Placeholder description.", 7.1, 102, "Emma Brooks"),
        Movie("Echoes of Tomorrow", "#117a65", 2024, "Placeholder description.", 8.7, 136, "Michael Reed"),
        Movie("Silver Lining", "#7d6608", 2019, "Placeholder description.", 6.9, 95, "Laura Scott"),
        Movie("The Long Road", "#6c3483", 2022, "Placeholder description.", 7.8, 128, "Ryan Turner"),
        Movie("Starlight", "#1b4f72", 2023, "Placeholder description.", 8.4, 115, "Natalie King"),
        Movie("Midnight Rain", "#922b21", 2021, "Placeholder description.", 7.3, 107, "Daniel White"),
        Movie("Shadow Realm", "#0e6655", 2024, "Placeholder description.", 8.9, 142, "Sophia Green"),
    ],

    "Popular Movies": [
        Movie("Midnight Express", "#922b21", 2022, "Placeholder description.", 7.9, 121, "James Carter"),
        Movie("Ocean Deep", "#1a5276", 2020, "Placeholder description.", 8.1, 117, "Sarah Mitchell"),
        Movie("Desert Storm", "#b9770e", 2023, "Placeholder description.", 7.4, 109, "David Ross"),
        Movie("Urban Legends", "#512e5f", 2021, "Placeholder description.", 7.8, 113, "Emma Brooks"),
        Movie("Hidden Depths", "#148f77", 2024, "Placeholder description.", 8.6, 131, "Michael Reed"),
        Movie("Wildfire", "#a93226", 2019, "Placeholder description.", 7.2, 104, "Laura Scott"),
        Movie("Paper Moon", "#7d3c98", 2022, "Placeholder description.", 8.0, 118, "Ryan Turner"),
        Movie("Open Skies", "#2e86c1", 2023, "Placeholder description.", 7.7, 112, "Natalie King"),
        Movie("Thunderstrike", "#7b241c", 2021, "Placeholder description.", 8.3, 126, "Daniel White"),
        Movie("Iron Will", "#1b4f72", 2024, "Placeholder description.", 8.5, 134, "Sophia Green"),
    ],

    "Popular TV Series": [
        TVShow("Crown & Glory", "#6c3483", 2021, "Placeholder description.", 8.8, 5, 10),
        TVShow("Shadow Unit", "#1b4f72", 2020, "Placeholder description.", 8.3, 4, 12),
        TVShow("Crystal Lake", "#0e6655", 2022, "Placeholder description.", 7.9, 3, 8),
        TVShow("Iron Circuit", "#7b241c", 2023, "Placeholder description.", 8.5, 2, 10),
        TVShow("Neon Nights", "#4a235a", 2021, "Placeholder description.", 8.1, 4, 10),
        TVShow("Sapphire Skies", "#154360", 2019, "Placeholder description.", 7.8, 6, 8),
        TVShow("Thunder Alley", "#935116", 2024, "Placeholder description.", 8.7, 2, 12),
        TVShow("Winter Frost", "#1a5276", 2020, "Placeholder description.", 8.0, 5, 10),
        TVShow("Ember Falls", "#922b21", 2022, "Placeholder description.", 8.4, 3, 12),
        TVShow("Ghost Protocol", "#4a235a", 2023, "Placeholder description.", 8.6, 2, 8),
    ],

    "Action & Adventure": [
        Movie("Thunderstrike", "#922b21", 2021, "Placeholder description.", 8.3, 126, "Daniel White"),
        Movie("Force Majeure", "#1b4332", 2022, "Placeholder description.", 7.9, 119, "James Carter"),
        Movie("Bulletproof", "#4a235a", 2023, "Placeholder description.", 7.5, 108, "Sarah Mitchell"),
        Movie("Rapid Fire", "#b9770e", 2024, "Placeholder description.", 8.2, 123, "David Ross"),
        Movie("Impact Zone", "#7b241c", 2020, "Placeholder description.", 7.8, 115, "Emma Brooks"),
        Movie("Renegade", "#1a5276", 2022, "Placeholder description.", 8.1, 127, "Michael Reed"),
        Movie("Lock & Load", "#935116", 2021, "Placeholder description.", 7.4, 111, "Laura Scott"),
        Movie("Blitz", "#0e6655", 2024, "Placeholder description.", 8.5, 132, "Ryan Turner"),
    ],

    "Comedy": [
        Movie("Laugh Track", "#7d6608", 2022, "Placeholder description.", 7.8, 98, "Natalie King"),
        Movie("Funny Business", "#117a65", 2021, "Placeholder description.", 7.4, 102, "Daniel White"),
        Movie("Comedy Gold", "#6c3483", 2023, "Placeholder description.", 8.0, 105, "Sophia Green"),
        Movie("Stand Up", "#b7950b", 2020, "Placeholder description.", 7.1, 93, "James Carter"),
        Movie("Hilarious", "#1a5276", 2024, "Placeholder description.", 8.4, 107, "Sarah Mitchell"),
        Movie("Comic Relief", "#935116", 2019, "Placeholder description.", 7.6, 100, "David Ross"),
        Movie("Joke's On You", "#922b21", 2022, "Placeholder description.", 7.9, 96, "Emma Brooks"),
        Movie("Lighthearted", "#148f77", 2023, "Placeholder description.", 8.1, 103, "Michael Reed"),
    ],

    "Drama": [
        Movie("Broken Pieces", "#6c3483", 2021, "Placeholder description.", 8.4, 124, "Laura Scott"),
        Movie("Silent Echo", "#1a5276", 2022, "Placeholder description.", 8.1, 118, "Ryan Turner"),
        Movie("The Divide", "#7b241c", 2020, "Placeholder description.", 7.7, 121, "Natalie King"),
        Movie("Fading Light", "#b9770e", 2023, "Placeholder description.", 8.3, 130, "Daniel White"),
        Movie("Tender Is the Night", "#117a65", 2024, "Placeholder description.", 8.7, 135, "Sophia Green"),
        Movie("Crossroads", "#935116", 2021, "Placeholder description.", 7.9, 116, "James Carter"),
        Movie("Aftermath", "#4a235a", 2022, "Placeholder description.", 8.2, 122, "Sarah Mitchell"),
        Movie("Memoir", "#922b21", 2020, "Placeholder description.", 7.8, 114, "David Ross"),
    ],

    "Documentaries": [
        Movie("Blue Planet", "#1a5276", 2023, "Placeholder description.", 9.1, 88, "Emma Brooks"),
        Movie("Nature's Call", "#0e6655", 2022, "Placeholder description.", 8.8, 92, "Michael Reed"),
        Movie("Ancient Worlds", "#6c3483", 2021, "Placeholder description.", 8.6, 95, "Laura Scott"),
        Movie("Deep Dive", "#148f77", 2024, "Placeholder description.", 8.9, 90, "Ryan Turner"),
        Movie("Unsolved", "#4a235a", 2020, "Placeholder description.", 8.2, 84, "Natalie King"),
        Movie("Through the Lens", "#7d6608", 2022, "Placeholder description.", 8.5, 89, "Daniel White"),
        Movie("True Stories", "#922b21", 2023, "Placeholder description.", 8.7, 93, "Sophia Green"),
        Movie("Horizons", "#1b4f72", 2021, "Placeholder description.", 8.4, 87, "James Carter"),
    ],
}