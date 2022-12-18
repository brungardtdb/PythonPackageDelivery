import Data_Access.location_reader as lr
import Data_Access.package_reader as pr
import Repositories.Package_Repository.package_repository as package_repository
import Package_Delivery.delivery_service as ds
import Cmd.command_processor as cmd

# is this right?...
# Total time complexity: O((n^2 * (n + v + (v^2 + v * e) + (v + e + (v^2 + v * e)) + v + n)
# Total space complexity: O((v^2 + v * e) + n * (v + e) + n) + (v^2 + v * e))
if __name__ == '__main__':
    # get packages and locations
    location_graph = lr.get_locations()                            # Time -> O(v^2) Space -> O(v + e)
    packages = pr.get_packages()                                   # Time -> O(n)   Space -> O(n)
    # create package repo for easy lookup
    package_repo = package_repository.PackageRepository(packages)  # Time -> O(n)   Space -> O(n)
    # initialize delivery service and deliver all packages
    service = ds.DeliveryService(package_repo)                     # Time -> O(1)   Space -> O(n)

    service.deliver_packages(location_graph)
    # Time: O((n^2 * (n + v + (v^2 + v * e) + (v + e + (v^2 + v * e)) + v + n)
    # Space: O((v^2 + v * e) + n * (v + e) + n) + (v^2 + v * e))

    cmd.print_help()
    sentinel = True
    # making the assumption here that all commands will run once
    # there is no telling how many commands a user will enter
    # so, I will not factor that into the time complexity or space complexity
    while sentinel:  # listen for commands until user is done entering commands
        command = input("")
        if not cmd.command_is_valid(command):  # O(1), O(n)
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
            continue                    # O(n), O(1)
        # print status for package(s)
        cmd.process_pstatus(command, package_repo)  # O(n + n^2), O(n)

        # G.  Provide an interface for the user to view the status and info (as listed in part F)
        # of any package at any time, and the total mileage traveled by all trucks.
        # (The delivery status should report the package as at the hub, en route, or delivered.
        # Delivery status must include the time.)
