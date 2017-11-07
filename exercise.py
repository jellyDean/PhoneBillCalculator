from datetime import datetime
import math
import collections

#phone_log_input = '00:01:07,400-234-090\n00:05:01,701-080-080\n00:05:00,400-234-090'
phone_log_input = "00:10:07,400-234-090\n" \
                  "00:05:01,701-080-080\n" \
                  "00:05:00,400-234-090\n" \
                  "00:15:00,123-234-090\n" \
                  "00:05:00,400-234-090\n" \
                  "00:15:00,123-234-090\n" \
                  "00:05:00,400-234-090\n" \
                  "00:15:00,123-234-090\n" \
                  "00:05:00,400-234-090\n" \
                  "00:15:00,123-234-090\n" \
                  "00:15:00,123-234-090\n" \
                  "00:20:00,458-234-090"

# parse the input
list_of_phone_calls = phone_log_input.split("\n")

phone_number_and_duration_dict = {}
for phone_call in list_of_phone_calls:
    splitter = phone_call.split(",")
    duration = splitter[0]
    phone_number = splitter[1]

    # TODO: add exception handling in case of bad input that cannot be parsed
    # convert times to datetime objects so that they are easier to work with
    datetimeobject = datetime.strptime(duration, '%H:%M:%S')

    # Datetime object needs a year to do a time delta. Default is 1900-01-01
    delta_date = datetime(1900, 01, 01)

    # create dict that has multiple calls per phone number {"123-456-344":[00:05:01, 00:06:03]....}
    duration_dict = phone_number_and_duration_dict.setdefault(phone_number, [])
    duration_dict.append((datetimeobject - delta_date).total_seconds())

total_calls_and_duration_dict = {}
total_calls_and_cost_dict = {}
longest_phone_call_duration = 0

# apply rules for calculating cost and prep for duplicate high usage costs
for phone_number in phone_number_and_duration_dict:
    total_cost_for_call = 0
    list_of_durations_in_seconds = phone_number_and_duration_dict[phone_number]
    total_duration_in_seconds = 0

    # calculate total cost of call in seconds
    for call_in_seconds in list_of_durations_in_seconds:
        total_duration_in_seconds += call_in_seconds

    total_duration_in_minutes = total_duration_in_seconds / 60

    # apply rules
    if total_duration_in_minutes < 5:
        total_cost_for_call = total_duration_in_seconds * 3
    else:
        # grab ceiling in case its 5.01 round to 6 and charge
        minute_ceiling = math.ceil(total_duration_in_minutes)
        total_cost_for_call = minute_ceiling * 150

    if total_duration_in_seconds > longest_phone_call_duration:
        longest_phone_call_duration = total_duration_in_seconds

    # change phone to numeric for last rule to be applied. This was a tad tricky, id most likely refactor the way this
    # was done but time is of the essence
    phone_numeric_value = int(phone_number.replace("-",""))
    total_calls_and_duration_dict[phone_numeric_value] = total_duration_in_seconds
    total_calls_and_cost_dict[phone_numeric_value] = total_cost_for_call


# check to see if their are duplicate phone calls that share the highest duration
duplicate_duration_dict = {}
for phone_number in total_calls_and_duration_dict:
    total_duration_in_seconds = total_calls_and_duration_dict[phone_number]
    # check if the highest duration(s) were found. if so store them for later processing
    if total_duration_in_seconds == longest_phone_call_duration:
        duplicate_duration_dict[phone_number] = total_duration_in_seconds


# get phone number with highest duration and smallest numerical value
od = collections.OrderedDict(sorted(duplicate_duration_dict.items()))
free_phone_call_tuple = od.items()[0]
free_phone_call_number = free_phone_call_tuple[0]

# remove the promotional call from the cost
total_calls_and_cost_dict.pop(free_phone_call_number)

# print total cost in cents
print sum(total_calls_and_cost_dict.values())

