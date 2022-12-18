from datetime import datetime
from Enums.delivery_status import DeliveryStatus


class Package:

    def __init__(self,
                 package_id,
                 address,
                 city,
                 zip_code,
                 delivery_deadline,
                 mass_kilo,
                 special_notes='',
                 state='UT'):  # All packages located in Utah
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kilo = mass_kilo
        self.special_notes = special_notes
        self.delivery_status = DeliveryStatus.AT_THE_HUB  # By default, packages are located at the hub
        self.delivery_time = datetime.min  # default to min until delivered
        self.start_time = datetime.min  # default to min until package has left the hub
        self.truck_id = -1  # initialized to -1 which will indicate package has not been loaded onto truck
