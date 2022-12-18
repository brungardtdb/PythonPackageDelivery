import Package_Status.package_status as ps
import User_Time.user_time as ut


# function that validates if the command a user has entered is valid
# Time: O(1)
# Space: O(n)
def command_is_valid(cmd):
    segs = cmd.split(" ")
    c = segs[0].lower()
    # if mileage, help, or quit, no further processing necessary
    if c == "mileage" or c == "h" or c == "q":
        return True
    # pstatus command should have 4 components separated by space
    if len(segs) != 4:
        return False
    if c != "pstatus":
        return False
    # check if user specified 'all' or an id for a specific package
    id_segs = segs[1].split("=")
    if id_segs[0].lower() != "-all" and id_segs[0].lower() != "-id":
        return False
    time_segs = segs[2].split("=")
    # ensure time was given
    if time_segs[0].lower() != "-time":
        return False
    am_pm = segs[3]
    # validate time format
    if am_pm.lower() != "am" and am_pm.lower() != "a.m." and \
            am_pm.lower() != "pm" and am_pm.lower() != "p.m.":
        return False
    time = time_segs[1] + " " + am_pm
    if not ut.time_is_valid(time):
        return False
    return True


# function that processes pstatus command
# Time: O(n + n^2)
# Space: O(n)
def process_pstatus(cmd, package_repo):
    segs = cmd.split(" ")
    # get user requested time
    time_segs = segs[2].split("=")
    t = time_segs[1] + " " + segs[3]
    time = ut.get_user_defined_time(t)  # O(n), O(n)
    id_segs = segs[1].split("=")
    id_arg = id_segs[0].lower()
    # determine if all packages requested or a single package
    if id_arg == "-all":  # if user requests status for all packages
        print("Status for all packages at " + t)
        ps.get_status_of_all_packages_at_time(package_repo, time)  # O(n^2), O(1)
    elif id_arg == "-id":  # if user requests status for a specific package
        pkgid = int(id_segs[1])
        p = package_repo.get_package_by_id(pkgid)  # O(n), O(1)
        print("Status for package " + str(pkgid) + " at " + t)
        ps.get_package_at_time(p, time)


# prints command line help instructions
# Time: O(1)
# Space: O(1)
def print_help():
    print("Usage: COMMAND [ARG...]")
    print("To view all packages at a given time, enter: ")
    print("\t \"pstatus -all -time={HH:MM [AM/PM]}\"")
    print("To view a package at a given time, enter: ")
    print("\t \"pstatus -id={id} -time={HH:MM [AM/PM]}\"")
    print("To view total truck mileage, enter: ")
    print("\t \"mileage\"")
    print("To view help, enter: ")
    print("\t \"h\"")
    print("To quit, enter: ")
    print("\t \"q\"")
