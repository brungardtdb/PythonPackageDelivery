import Data_Access.location_reader as lr
import Data_Access.package_reader as pr
import Repositories.Package_Repository.package_repository as package_repository
import Package_Delivery.delivery_service as ds
import Cmd.command_processor as cmd

# Total time complexity: O(n^2 * v^2)
# Total space complexity: O(n + v^2)
if __name__ == '__main__':
    # get packages and locations
    location_graph = lr.get_locations()
    packages = pr.get_packages()
    # create package repo for easy lookup
    package_repo = package_repository.PackageRepository(packages)
    # initialize delivery service and deliver all packages
    service = ds.DeliveryService(package_repo)
    service.deliver_packages(location_graph)

    cmd.print_help()
    sentinel = True
    while sentinel:  # listen for commands until user is done entering commands
        command = input("")
        if not cmd.command_is_valid(command):
            if command.split(" ")[0].lower() == "pstatus":
                print("\"pstatus\" command requires two additional arguments "
                      "and time format must match {HH:MM [AM/PM]}")
            else:
                print("Please enter a valid command.")
            continue
        # quit the application
        if command.lower() == "q":
            sentinel = False
            continue
        # print help for command line
        if command.lower() == "h":
            cmd.print_help()
            continue
        # print mileage for all trucks
        if command.lower() == "mileage":
            print("Total Miles: " + str(service.get_total_truck_mileage()))
            continue
        # print status for package(s)
        cmd.process_pstatus(command, package_repo)

        # G.  Provide an interface for the user to view the status and info (as listed in part F)
        # of any package at any time, and the total mileage traveled by all trucks.
        # (The delivery status should report the package as at the hub, en route, or delivered.
        # Delivery status must include the time.)
