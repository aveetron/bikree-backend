from typing import Dict, Any


class SerializerHelper:
    def __init__(self, obj: Any):
        self.obj = obj


class UserSerializerHelper(SerializerHelper):

    def get_created_by(self) -> Dict[str, any]:
        return {
            "uid": self.obj.uid.hex if self.obj else None,
            "full_name": {
                "first": self.obj.first_name if self.obj.first_name else None,
                "last": self.obj.last_name if self.obj.last_name else None,
            },
            "role": self.obj.role.name if self.obj.role else None,
        }

    def get_updated_by(self) -> Dict[str, any]:
        return {
            "uid": self.obj.uid.hex if self.obj else None,
            "full_name": {
                "first": self.obj.first_name if self.obj.first_name else None,
                "last": self.obj.last_name if self.obj.last_name else None,
            },
            "role": self.obj.role.name if self.obj.role else None,
        }


class InventorySerializerHelper(SerializerHelper):

    def get_inventory(self) -> Dict[str, any]:
        return {
            "name": self.obj.name if self.obj else None,
            "description": self.obj.description if self.obj else None,
            "location": {
                "position": self.obj.position if self.obj else None,
                "floor": self.obj.floor if self.obj else None,
                "rack": self.obj.rack if self.obj else None,
            },
        }


class ShopSerializerHelper(SerializerHelper):

    def get_shop(self) -> Dict[str, any]:
        return {
            "uid": self.obj.uid.hex if self.obj else None,
            "name": self.obj.name if self.obj else None,
        }
