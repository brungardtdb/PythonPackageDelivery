from datetime import datetime
import Package_Delivery.delivery_truck as delivery_truck


# class to manage the delivering of packages
class DeliveryService:

    def __init__(self, package_repo):
        self.repo = package_repo
        self.first_truck = delivery_truck.DeliveryTruck()
        self.first_truck.truck_id = 1
        self.second_truck = delivery_truck.DeliveryTruck()
        self.second_truck.truck_id = 2
        self.third_truck = delivery_truck.DeliveryTruck()
        self.third_truck.truck_id = 3
        self.delivery_trucks = [self.first_truck, self.second_truck, self.third_truck]
        self.wrong_address = self.repo.get_packages_by_special_notes("Wrong address listed")
        self.delivered_packages = []

    # method for delivering all packages on all delivery trucks
    def deliver_packages(self, graph):
        # load truck one and deliver all packages
        self._load_truck_one()
        first_start_time = datetime.strptime('8:00', '%H:%M').time()
        self.first_truck.deliver_all_packages(graph, first_start_time, True)
        # load truck two and deliver all packages
        self._load_truck_two()
        second_start_time = datetime.strptime('9:05', '%H:%M').time()
        self.second_truck.deliver_all_packages(graph, second_start_time, False)
        # load truck three and deliver all packages after correcting
        # incorrect package address
        self._load_truck_three()
        earliest_possible_time = datetime.strptime('10:20', '%H:%M').time()
        third_start_time = self.first_truck.finish_time \
            if self.first_truck.finish_time > earliest_possible_time \
            else earliest_possible_time
        self._correct_incorrect_package_address()
        self.third_truck.deliver_all_packages(graph, third_start_time, False)

    # method for loading a package onto a delivery truck
    def _load_package_on_truck(self, pkg, truck):
        if pkg.id in self.delivered_packages:
            return
        truck.add_package_to_truck(pkg)
        self.delivered_packages.append(pkg.id)

    # extremely ad hoc method for loading truck 1
    def _load_truck_one(self):
        packages = [
            self.repo.get_package_by_id(1),
            self.repo.get_package_by_id(5),
            self.repo.get_package_by_id(7),
            self.repo.get_package_by_id(8),
            self.repo.get_package_by_id(13),
            self.repo.get_package_by_id(14),
            self.repo.get_package_by_id(15),
            self.repo.get_package_by_id(16),
            self.repo.get_package_by_id(19),
            self.repo.get_package_by_id(20),
            self.repo.get_package_by_id(21),
            self.repo.get_package_by_id(29),
            self.repo.get_package_by_id(30),
            self.repo.get_package_by_id(34),
            self.repo.get_package_by_id(37),
            self.repo.get_package_by_id(39),
        ]
        for p in packages:
            self._load_package_on_truck(p, self.first_truck)

    # extremely ad hoc method for loading truck 2
    def _load_truck_two(self):
        packages = [
            self.repo.get_package_by_id(2),
            self.repo.get_package_by_id(3),
            self.repo.get_package_by_id(4),
            self.repo.get_package_by_id(6),
            self.repo.get_package_by_id(10),
            self.repo.get_package_by_id(18),
            self.repo.get_package_by_id(25),
            self.repo.get_package_by_id(26),
            self.repo.get_package_by_id(27),
            self.repo.get_package_by_id(31),
            self.repo.get_package_by_id(32),
            self.repo.get_package_by_id(33),
            self.repo.get_package_by_id(35),
            self.repo.get_package_by_id(36),
            self.repo.get_package_by_id(38),
            self.repo.get_package_by_id(40)
        ]
        for p in packages:
            self._load_package_on_truck(p, self.second_truck)

    # extremely ad hoc method for loading truck 3
    def _load_truck_three(self):
        packages = [
            self.repo.get_package_by_id(9),
            self.repo.get_package_by_id(11),
            self.repo.get_package_by_id(12),
            self.repo.get_package_by_id(17),
            self.repo.get_package_by_id(22),
            self.repo.get_package_by_id(23),
            self.repo.get_package_by_id(24),
            self.repo.get_package_by_id(28)
        ]
        for p in packages:
            self._load_package_on_truck(p, self.third_truck)

    # extremely ad hoc method for correcting incorrect address on package 9
    def _correct_incorrect_package_address(self):
        # eventually these will need to come from a file or database
        # so this is less ad hoc
        correct_address = "410 South State St"
        correct_city = "Salt Lake City"
        correct_zip = "84111"
        for pkg in self.wrong_address:
            pkg.address = correct_address
            pkg.zip_code = correct_zip
            pkg.city = correct_city

    # method to get truck mileage
    def get_truck_mileage(self, truck_id):
        match truck_id:
            case self.first_truck.truck_id:
                return self.first_truck.total_mileage
            case self.second_truck.truck_id:
                return self.second_truck.total_mileage
            case self.third_truck.truck_id:
                return self.third_truck.total_mileage
            case default:
                return None

    # method to get mileage for all trucks
    def get_total_truck_mileage(self):
        total = 0.0
        for truck in self.delivery_trucks:
            total += self.get_truck_mileage(truck.truck_id)
        return total
