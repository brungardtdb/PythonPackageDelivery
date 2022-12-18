from datetime import datetime
import re


# parses a string provided by a user and returns the corresponding time
# Time: O(n) where n is the number of characters in the string
# Space: O(n) for creating list from string segments
def get_user_defined_time(time):
    segs = time.split(" ")
    # if time is am, just pass in whatever time user provided
    if segs[1].lower() != "p.m." and segs[1].lower() != "pm":
        return datetime.strptime(segs[0], '%H:%M').time()
    else:  # add additional 12 hours to account for time in the afternoon
        time_segs = segs[0].split(":")
        hr = time_segs[0]
        if int(hr) >= 12:  # if pm time is noon or later than 12 (military time)
            return datetime.strptime(segs[0], "%H:%M").time()  # just return time
        else:  # if pm time is provided less than noon, adjust time, so we can compare
            new_hr = int(hr) + 12
            new_time = str(new_hr) + ":" + time_segs[1]
            return datetime.strptime(new_time, "%H:%M").time()


# uses regular expression to verify time is in correct format
# Time: O(n) where n is the number of characters in the string
# Space: O(1)
# I have the complexity here, but I do not suspect asymptotic growth
# in the number of characters in a given time entered by the user, so I will not
# be adding this to the total unless I receive feedback telling me to do otherwise
def time_is_valid(time):
    first_pattern = re.compile("[0-2][0-9]:[0-5][0-9] [a|A|p|P][M|m]")
    second_pattern = re.compile("[0-2][0-9]:[0-5][0-9] [a|A|p|P].[M|m].")
    return first_pattern.match(time) or second_pattern.match(time)
