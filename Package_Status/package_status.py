import Enums.delivery_status


# function that displays the full status of a package at a given time
# Time: O(1)
# Space: O(1)
def get_package_at_time(pkg, time):
    print("Package ID: \t\t" + str(pkg.id))
    print("Delivery Address: \t" + pkg.address)
    print("Delivery Deadline: \t" + str(pkg.delivery_deadline))
    print("Delivery City: \t\t" + pkg.city)
    print("Delivery Zip: \t\t" + pkg.zip_code)
    print("Package \"Weight\": \t" + str(pkg.mass_kilo))
    s = get_delivery_status_at_time(pkg, time)
    print("Package Status: \t" + get_status_string(s))
    print("Delivery Time: \t\t" + str(pkg.delivery_time))


# function that displays a summarized status of all packages at a given time
# Time: O(n^2)
# Space: O(1)
def get_status_of_all_packages_at_time(package_repo, time):
    print_table_header_for_packages()
    for index in range(package_repo.packages.map_length):  # O(n)
        index += 1
        p = package_repo.get_package_by_id(index)  # O(n), O(1)
        display_package_status(p, time)


# function for printing the table header when displaying status summary
# for all delivered packages
# Time: O(1)
# Space: O(1)
def print_table_header_for_packages():
    print("Package ID: \tDelivery Address "
          "\t\t\t\t\t\t\tDelivery Status "
          "\t\tDelivery Time "
          "\t On Time"
          "\t\tTruck ID")
    print()

# function that displays a summarized package status at a given time
# Time: O(1)
# Space: O(1)
def display_package_status(pkg, time):
    status_at_time = get_delivery_status_at_time(pkg, time)
    s = get_status_string(status_at_time)
    on_time = False
    if pkg.delivery_deadline == "EOD":
        on_time = True
    elif pkg.delivery_deadline > pkg.delivery_time:
        on_time = True
    print("{: <11}".format(str(pkg.id)) +
          "\t\t" + "{: <40}".format(pkg.address) +
          "\t" + "{: <16}".format(s) + "\t\t" +
          str(pkg.delivery_time) + "\t\t" +
          "  " + str(on_time) + "\t\t\t" +
          str(pkg.truck_id))


# function that converts delivery status to a string
# Time : O(1)
# Space: O(1)
def get_status_string(status):
    match status:
        case Enums.delivery_status.DeliveryStatus.DELIVERED:
            return "Delivered"
        case Enums.delivery_status.DeliveryStatus.EN_ROUTE:
            return "En Route"
        case Enums.delivery_status.DeliveryStatus.AT_THE_HUB:
            return "At the Hub"


# Gets the delivery status of a package at a given time
# Time: O(1)
# Space: O(1)
def get_delivery_status_at_time(package, time):
    if time < package.start_time:
        return Enums.delivery_status.DeliveryStatus.AT_THE_HUB
    if package.start_time <= time < package.delivery_time:
        return Enums.delivery_status.DeliveryStatus.EN_ROUTE
    if time >= package.delivery_time:
        return Enums.delivery_status.DeliveryStatus.DELIVERED
