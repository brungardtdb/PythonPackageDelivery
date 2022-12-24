# function that replaces single characters N, W, E, S with the word indicating the direction
# used to make addresses consistent and easier to work with
def patch_package_address(addr):
    addr_segments = addr.split(" ")
    return_address = ""
    for seg in addr_segments:
        if seg == "S":
            return_address += "South"
        elif seg == "W":
            return_address += "West"
        elif seg == "E":
            return_address += "East"
        elif seg == "N":
            return_address += "North"
        else:
            return_address += seg
        return_address += " "
    stripped_address = return_address.strip()
    return stripped_address
