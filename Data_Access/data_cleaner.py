# function that replaces single characters N, W, E, S with the word indicating the direction
# used to make addresses consistent and easier to work with
def patch_package_address(addr):
    # Time O(n) where n is the number of characters in the address
    # Space O(1) since we are only replacing characters
    # I have the complexity here, but I do not suspect asymptotic growth
    # in the number of characters in a package address, so I will not
    # be adding this to the total unless I receive feedback telling me to do otherwise
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
