from enum import Enum


# enum used to represent delivery status for packages
class DeliveryStatus(Enum):
    AT_THE_HUB = 0
    EN_ROUTE = 1
    DELIVERED = 2

    def to_string(self):
        if self.AT_THE_HUB:
            return "at the hub"
        if self.EN_ROUTE:
            return "en route"
        if self.DELIVERED:
            return "delivered"
