import requests
from typing import List
from models import Hotel, Location, Amenities, Images
from utils import Utils

class BaseSupplier:
    @staticmethod
    def endpoint() -> str:
        """URL to fetch supplier data"""
        raise NotImplementedError

    @staticmethod
    def parse(obj: dict) -> Hotel:
        """Parse supplier-provided data into Hotel object"""
        raise NotImplementedError

    def fetch(self) -> List[Hotel]:
        url = self.endpoint()
        resp = requests.get(url)
        resp.raise_for_status()
        return [self.parse(dto) for dto in resp.json()]
    

class Acme(BaseSupplier):
    @staticmethod
    def endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        amenities = Utils.get_collection(dto, ['Facilities'], [])
        return Hotel(
            id = dto.get('Id'),
            destination_id = dto.get('DestinationId'),
            name = Utils.get_value(dto, 'Name'),
            description = Utils.get_value(dto, 'Description'),
            location = Location(
                address = Utils.get_value(dto, 'Address'),
                city = Utils.get_value(dto, 'City'),
                country = Utils.get_value(dto, 'Country'),
                lat = Utils.get_value(dto, 'Latitude'),
                lng = Utils.get_value(dto, 'Longitude')
            ),
            amenities = Amenities(
                general = Utils.format_amenities(amenities),
            ),
            images = Images(),
            booking_conditions = []
        )

class Patagonia(BaseSupplier):
    @staticmethod
    def endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        images = Utils.get_collection(dto, ['images'], {})
        amenities = Utils.get_collection(dto, ['amenities'], default = [])
        return Hotel(
            id = dto.get('id'),
            destination_id = dto.get('destination'),
            name = Utils.get_value(dto, 'name'),
            description = Utils.get_value(dto, 'info'),
            location = Location(
                address = Utils.get_value(dto, 'address'),
                city = Utils.get_value(dto, 'city'),
                country = Utils.get_value(dto, 'country'),
                lat = Utils.get_value(dto, 'lat'),
                lng = Utils.get_value(dto, 'lng')
            ),
            amenities = Amenities(
                general = Utils.format_amenities(amenities)
            ),
            images = Images(
                rooms = Utils.get_images(Utils.get_collection(images, ['rooms'], []), {'link': 'url', 'description': 'description'}),
                amenities = Utils.get_images(Utils.get_collection(images, ['amenities'], []), {'link': 'url', 'description': 'description'}),
                site = Utils.get_images(Utils.get_collection(images, ['url'], []), {'link': 'url', 'description': 'description'})
            ),
            booking_conditions = []
        )

class Paperflies(BaseSupplier):
    @staticmethod
    def endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        location = Utils.get_collection(dto, ['location'], {})
        images = Utils.get_collection(dto, ['images'], {})
        booking_conditions = Utils.get_collection(dto, ['booking_conditions'], [])

        return Hotel(
            id = dto.get('hotel_id'),
            destination_id = dto.get('destination_id'),
            name = Utils.get_value(dto, 'name'),
            description = Utils.get_value(dto, 'description'),
            location = Location(
                address = Utils.get_value(location, 'address'),
                city = Utils.get_value(location, 'city'),
                country = Utils.get_value(location, 'country'),
                lat = Utils.get_value(location, 'lat'),
                lng = Utils.get_value(location, 'lng')
            ),
            amenities = Amenities(
                general = Utils.format_amenities(Utils.get_collection(dto, ['amenities', 'general'], [])),
                room = Utils.format_amenities(Utils.get_collection(dto, ['amenities', 'room'], []))
            ),
            images = Images(
                rooms = Utils.get_images(Utils.get_collection(images, ['rooms'], []), {'link': 'link', 'description': 'caption'}),
                amenities = Utils.get_images(Utils.get_collection(images, ['amenities'], []), {'link': 'link', 'description': 'caption'}),
                site = Utils.get_images(Utils.get_collection(images, ['site'], []), {'link': 'link', 'description': 'caption'})
            ),
            booking_conditions = booking_conditions
        )