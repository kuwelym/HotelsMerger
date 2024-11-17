from dataclasses import dataclass, field
from utils import Utils
from typing import List

@dataclass
class Location:
    address: str
    city: str = ""
    country: str = ""
    lat: float = 0.0
    lng: float = 0.0

    def __or__(self, other: 'Location') -> 'Location':
        '''
        Merge two locations, prioritizing non-empty fields and longer strings
        '''
        self.address = Utils.merge_str_field(self.address, other.address)
        self.city = Utils.merge_str_field(self.city, other.city)
        self.country = Utils.merge_str_field(self.country, other.country)
        self.lat = self.lat or other.lat
        self.lng = self.lng or other.lng
        return self

@dataclass
class Amenities:
    general: List[str] = field(default_factory = list)
    room: List[str] = field(default_factory = list)

    def __add__(self, other):
        def normalize_list(items):
            '''
            Only keep unique items in a list, ignoring case and spaces
            '''
            seen = {}
            for item in items:
                normalized = item.strip().lower().replace(" ", "")
                if normalized not in seen:
                    seen[normalized] = item
            return list(seen.values())

        combined_general = normalize_list((self.general or []) + (other.general or []))
        combined_room = normalize_list((self.room or []) + (other.room or []))

        # prioritize putting in the room amenities category than the general one
        combined_general = [
            amenity for amenity in combined_general 
            if amenity.strip().lower().replace(" ", "") not in map(
                lambda x: x.strip().lower().replace(" ", ""), combined_room
            )
        ]
        self.general = combined_general
        self.room = combined_room
        return self

@dataclass
class Image:
    link: str
    description: str

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.link == other.link
        return False

    def __hash__(self):
        return hash(self.link)

@dataclass
class Images:
    rooms: List[Image] = field(default_factory = list)
    site: List[Image] = field(default_factory = list)
    amenities: List[Image] = field(default_factory = list)

    def __add__(self, other):
        self.rooms = sorted(list(set((self.rooms or []) + (other.rooms or []))), key = lambda x: x.link)
        self.site = sorted(list(set((self.site or []) + (other.site or []))), key = lambda x: x.link)
        self.amenities = sorted(list(set((self.amenities or []) + (other.amenities or []))), key = lambda x: x.link)
        return self

@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    location: Location
    description: str
    amenities: Amenities
    images: Images
    booking_conditions: set[str] = field(default_factory = set)

    def merge(self, other: 'Hotel') -> 'Hotel':
        '''
        Merge two hotels, prioritizing non-empty fields and longer strings
        '''
        self.name = Utils.merge_str_field(self.name, other.name)
        self.location = self.location | other.location
        self.description = Utils.merge_str_field(self.description, other.description)
        self.amenities += other.amenities
        self.images += other.images
        self.booking_conditions += other.booking_conditions
        return self