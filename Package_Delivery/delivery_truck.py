import datetime
import math
import Enums.delivery_status


# updates package status to reflect that package has been delivered
# Time: O(1)
# Space: O(1)
def _update_package_status(pkg, delivery_time):
    pkg.delivery_time = delivery_time
    pkg.delivery_status = Enums.delivery_status.DeliveryStatus.DELIVERED


# helper method to indicate whether shortest path was found
# adds edges for shortest path to path_to_dest list
# Time: O(v + e) in the case that each vertex and edge exists in potential path
# Space: O(v + e) in the case that all vertices and edges are added to path
def _shortest_path_found(potential_paths, path_to_dest):
    chosen_path = None
    lowest_cost = math.inf
    # loop through potential paths to destination
    for path in potential_paths:
        local_cost = 0
        for edge in path:
            local_cost += edge.weight
        if local_cost < lowest_cost:
            chosen_path = path
            lowest_cost = local_cost
    # if shortest path has been found, add to path_to_dest and return
    if chosen_path is not None:
        for edge in chosen_path:
            path_to_dest.insert(0, edge)
        return True
    return False


# class used to manage delivering packages
class DeliveryTruck:

    # Time: O(1)
    # Space: O(1)
    def __init__(self):
        self.packages = []
        self.delivered_packages = []
        self.visited_nodes = []
        self.current_node = None
        self.graph = None
        self.start_time = None
        self.current_time = None
        self.finish_time = None
        self.distance_traveled = 0
        self.num_packages = 0
        self.max_packages = 16
        self.is_full = False
        self.return_when_done = False
        self.total_mileage = 0
        self.truck_id = 0

    # method for adding a package to the truck
    # Time: O(1) to update package and add to truck
    # Space: O(1) since we are capped at 16 packages and this will not grow with the # of packages on a given truck
    def add_package_to_truck(self, package):
        # make sure we are within capacity, add package to truck if we are
        if self.is_full:
            raise Exception("Number of packages has exceeded trucks capacity")
        package.truck_id = self.truck_id
        self.packages.append(package)
        package.delivery_status = Enums.delivery_status.DeliveryStatus.EN_ROUTE
        self.num_packages += 1
        if self.num_packages is self.max_packages:
            self.is_full = True

    # method for delivering all packages on truck
    # Time: O((n^2 * (n + v + (v^2 + v * e) + (v + e + (v^2 + v * e)) + v + n)
    # Space: O((v^2 + v * e) + n * (v + e) + n) + (v^2 + v * e))
    def deliver_all_packages(self, graph, start_time, return_to_hub):
        # start at hub
        hub = graph.get_node(1)             # O(v), O(1)
        self.delivered_packages = []
        self.visited_nodes = []
        self.current_node = hub
        self.return_when_done = return_to_hub
        self.graph = graph
        self.start_time = start_time
        self.current_time = start_time
        # set start time for all packages
        for pkg in self.packages:           # O(n), O(1)
            pkg.start_time = self.start_time

        self._deliver_packages(self.packages)  # Time: O(n^2 * (n + v + (v^2 + v * e)) + v + e)
                                               # Space: O(v^2 + v * e) + n * (v + e) + n)
        if return_to_hub:  # Time:  O(v + e + (v^2 + v * e)) Space: O(v * (v + e))
            self._return_to_hub()  # leave the other two trucks at the location of the last delivery
            # returning these trucks to the hub is not cost-effective, we will just get two new trucks
            # for tomorrow's delivery

    # method to return truck to hub
    # Time: O(v + e + (v^2 + v * e))
    # Space: O(v * (v + e))
    def _return_to_hub(self):
        hub = self.graph.get_node(1)  # O(v), O(1)
        path_to_hub = []
        # if shortest path to hub has been found, return to hub
        # Time: O(v * (v + e)) Space: O(v * (v + e))
        if self._pkg_dest_found(self.current_node, hub.data.location_address, path_to_hub):
            self._go_to_hub(path_to_hub)  # O(e), O(1)

    # method to return truck to hub
    # Time: O(e)
    # Space: O(1)
    def _go_to_hub(self, path_to_hub):
        # move through each edge on the way back to the hub, calculating time and mileage for each
        for edge in path_to_hub:  # O(e)
            self.current_node = edge.first_node if edge.first_node.id is not self.current_node.id else edge.second_node
            self._calculate_time(edge.weight)
        # reset truck state
        self.packages.clear()
        self.num_packages = 0
        self.is_full = False

    # method for delivering packages
    # Time: O(n^2 * (n + v + (v^2 + v * e)) + v + e)
    # Space: O(v^2 + v * e) + n * (v + e) + n)
    def _deliver_packages(self, pkgs):
        # loop until all packages are delivered
        while len(self.delivered_packages) < self.num_packages:  # O(n)
            pkg_tracker = []
            # loop through packages, finding the closest one to deliver
            for pkg in pkgs:                          # O(n)
                path_to_dest = []
                # skip package if already delivered
                if pkg.id in self.delivered_packages:  # O(n)
                    continue                                                         # Time: O(v + (v * (v + e)))
                    # if we find route to package, add it to package tracker
                if self._package_route_found(self.current_node, pkg, path_to_dest):  # Space: O(v * (v + e))
                    pkg_tracker.append((pkg, path_to_dest))  # Space: O(n * (v + e)) in the event entire graph is stored
                    self.visited_nodes = []                  # for each package
                else:
                    #  could not find route
                    self.visited_nodes = []
                    print("Could not deliver package")
                    print("Package ID: " + str(pkg.id))
                    print("Package Address: " + pkg.address)
                    continue
            # deliver whichever package is closest
            self._deliver_lowest_cost_package(pkg_tracker)  # O(n * (v + e) + (n * e)), O(n)

    # method for delivering whichever package has the lowest cost
    # Time: O(n * (v + e) + (n * e))
    # Space: O(n)
    def _deliver_lowest_cost_package(self, pkg_tracker):
        lowest_cost_pkg = None
        lowest_cost_path = None
        lowest_cost = math.inf
        # loop through possible packages, and figure out which is closest
        for p in pkg_tracker:  # Time -> O(n)
            cost = 0
            for edge in p[1]:  # Time -> O(v + e) in the event we have the entire graph to traverse
                cost += edge.weight
            if cost < lowest_cost:
                lowest_cost_pkg = p[0]
                lowest_cost_path = p[1]
                lowest_cost = cost
        if lowest_cost_pkg is not None:  # if closest package is found, deliver the package
            self._deliver_package(lowest_cost_pkg, lowest_cost_path)  # O(n *  e), O(n)

    # method for delivering a given package
    # Time: O(n * e)
    # Space: O(n)
    def _deliver_package(self, pkg, path_to_dest):
        # loop through edges on the way to package destination
        # calculating time and mileage for each
        for edge in path_to_dest:  # Time -> O(e) since we are only traversing edges
            self.current_node = edge.first_node if edge.first_node.id is not self.current_node.id else edge.second_node
            self._calculate_time(edge.weight)
        # when we have arrived at the destination, update the package status and add to delivered packages
        _update_package_status(pkg, self.current_time)
        self.delivered_packages.append(pkg.id)
        other_packages = []
        # find other packages at this address
        for p in self.packages:  # O(n)
            if p.address == pkg.address and p.id is not pkg.id:
                other_packages.append(p)
        # if other packages exist at this address, deliver them as well
        if other_packages is not None and len(other_packages) > 0:
            self._deliver_other_packages(other_packages, self.current_time)  # O(n), O(n)

    # method for delivering other packages that are at the same location as a given package
    # provided the package has not already been delivered
    # Time: O(n)
    # Space: O(n)
    def _deliver_other_packages(self, other_packages, delivery_time):
        for p in other_packages: # O(n)
            if p.id not in self.delivered_packages:
                _update_package_status(p, delivery_time)
                self.delivered_packages.append(p.id)

    # method to indicate whether we were able to find a route to a package
    # while searching, populates path_to_dest list with the shortest destination to package
    # Time: O(v + (v * (v + e)))
    # Space: O(v * (v + e))
    def _package_route_found(self, current_node, pkg, path_to_dest):
        sp_node = self.graph.get_node(current_node.id)                   # O(v), O(1)
        return self._pkg_dest_found(sp_node, pkg.address, path_to_dest)  # O(v * (v + e)), O(v * (v + e))

    # helper method indicates whether package destination was found
    # Time: O(v * (v + e)) to iterate through all vertices and edges for each vertex
    # Space: O(v * (v + e)) we will recurse into this method for each vertex on graph, while we
    # perform this recursion, each method call will exist on call stack and potentially create a
    # list of all vertices and edges for each vertex
    def _pkg_dest_found(self, current_node, addr, path_to_dest):
        self.visited_nodes.append(current_node.id)
        potential_paths = []
        # iterate through edges and vertices,
        # looking for location address that matches package to account for direct connection
        for edge in current_node.edges:  # Time -> O(v + e) to traverse entire graph
            other_node = edge.first_node if edge.first_node.id is not current_node.id else edge.second_node
            if other_node.data.location_address == addr:
                potential_paths.append([edge])  # in the unlikely event we append the entire graph, Space -> O(v + e)
                break  # we will have at most one direct connection
        # iterate through edges and vertices,
        # recursing into this method with each new node to explore the graph
        # until graph is exhausted, and we have determined potential paths to package
        for edge in current_node.edges:  # Time -> O(v + e) to traverse entire graph
            other_node = edge.first_node if edge.first_node.id is not current_node.id else edge.second_node
            if other_node.id not in self.visited_nodes:
                current_path = []
                if self._pkg_dest_found(other_node, addr, current_path):
                    current_path.insert(0, edge)
                    potential_paths.append(current_path)
        # return shortest path out of all potential paths
        return _shortest_path_found(potential_paths, path_to_dest)  # O(v + e), O(v + e)

    # method for incrementing total mileage and calculating time it took to deliver a package
    # based on a constant speed of 18mph
    # Time: O(1)
    # Space: O(1)
    def _calculate_time(self, weight):
        # increment total mileage
        self.total_mileage += weight
        # get time offset from distance traveled
        hours = weight / 18  # speed is constant 18mph
        whole_hours = int(hours)
        minutes = weight / 0.3  # speed is constant 18mph
        minutes -= whole_hours * 60
        whole_minutes = int(minutes)
        seconds = weight / 0.005  # speed is constant 18mph
        seconds -= whole_minutes * 60
        whole_seconds = int(seconds)
        # add to current time
        new_hours = self.current_time.hour + whole_hours
        new_minutes = self.current_time.minute + whole_minutes
        new_seconds = self.current_time.second + whole_seconds
        # adjust if we are over 60 minutes or seconds, assuming hrs won't be greater than 24
        if new_seconds > 59:
            added_minutes = new_seconds // 60
            new_seconds -= (added_minutes * 60)
            new_minutes += added_minutes
        if new_minutes > 59:
            added_hrs = new_minutes // 60
            new_minutes -= (added_hrs * 60)
            new_hours += added_hrs

        self.current_time = datetime.time(new_hours, new_minutes, new_seconds)
        # a bit of redundancy because I want to know when the truck is finished
        # without relying on a variable called 'current_time'
        # should match current time at the end
        self.finish_time = datetime.time(new_hours, new_minutes, new_seconds)
