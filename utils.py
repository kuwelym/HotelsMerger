import re
from typing import List, Dict

class Utils:
    @staticmethod
    def get_collection(dct, keys, default = {}):
        '''
        Get a dict or a list of values from a dict
        '''
        for key in keys:
            dct = dct.get(key, default)
        return dct or default

    @staticmethod
    def get_value(dct, key):
        """
        Get a value from a nested dictionary and:
        - If the json value is null or 0.0 or '', it will be set to None
        - And also I want to indicate missing data if the value is null.
        """
        value = dct.get(key)
        if isinstance(value, str):
            return value.strip() or None
        elif isinstance(value, (float, int)):
            return value or None
        return value

    @staticmethod
    def format_amenities(amenities: List[str]) -> List[str]:
        '''
        Format a list of amenities by inserting spaces before capital letters 
        and lowercasing, stripping them. E.g. "BusinessCenter " -> "business center"
        '''
        formatted = []
        for amenity in amenities:
            formatted.append(re.sub(r'(?<!^)(?=[A-Z])', ' ', amenity).strip().title().lower())
        return formatted

    @staticmethod
    def get_images(images: List[Dict], key_map: Dict[str, str]) -> List:
        '''
        Get a list of images with map keys
        '''
        from models import Image
        return [
            Image(link = Utils.get_value(image, key_map['link']), description = Utils.get_value(image, key_map['description']))
            for image in images or []
        ]
        
    @staticmethod
    def merge_str_field(field: str, other_field: str) -> str:
        '''
        Merge two string fields, prioritizing non-empty fields and longer strings
        '''
        if not field or (other_field and len(other_field) > len(field)):
            return other_field
        return field