from datetime import datetime

def validate_line(line):
    format = "%H:%M:%S"
    splitter = line.split()
    ts = splitter[0]
    username = splitter[1]
    session = splitter[2]

    if len(splitter) != 3:
        return False

    try:
        datetime.strptime(ts, format)
    except ValueError:
        return False

    if not username.isalnum():
        return False

    if session not in ["Start", "End"]:
        return False

    return True

def calculate_diff_seconds(start_time, end_time):
    from datetime import datetime
    format = "%H:%M:%S"

    start_time_sec = start_time.split(":")
    end_time_sec = end_time.split(":")

    
    # start_secs = int(start_time_sec[0]) * 60 * 60 + int(start_time_sec[1]) * 60 + int(start_time_sec[2])
    # end_secs = int(end_time_sec[0]) * 60 * 60 + int(end_time_sec[1]) * 60 + int(end_time_sec[2])

    difference = datetime.strptime(end_time, format) - datetime.strptime(start_time, format)
    return int(difference.total_seconds())
    # return (end_secs - start_secs)

CHARLIE_RECORDS = [
    {'time_stamp': '14:02:05', 'session': 'End'},
    {'time_stamp': '14:03:02', 'session': 'Start'},
    {'time_stamp': '14:03:37', 'session': 'End'},
    {'time_stamp': '14:04:41', 'session': 'Start'}
    ]

user_sessions = {
    "charlie" : {"count" : 0, "seconds" : 0 },
    "alice" : {"count" : 0, "seconds" : 0 },
}

for idx,charlie_record in enumerate(CHARLIE_RECORDS[:]):
    
    if charlie_record["session"] == "Start" and idx <= (len(CHARLIE_RECORDS)-1):
        adder = (next(end for end in CHARLIE_RECORDS if end["session"] == "End"))
        user_sessions["charlie"]["count"] += 1
        user_sessions["charlie"]["seconds"] += calculate_diff_seconds(charlie_record["time_stamp"],adder["time_stamp"])
        CHARLIE_RECORDS.remove(adder)
        CHARLIE_RECORDS.remove(charlie_record)

for idx,charlie_record in enumerate(CHARLIE_RECORDS):
    if charlie_record["session"] == "End":
        user_sessions["charlie"]["count"] += 1
        user_sessions["charlie"]["seconds"] += calculate_diff_seconds("14:02:03",charlie_record["time_stamp"])
        
    else:
        user_sessions["charlie"]["count"] += 1
        user_sessions["charlie"]["seconds"] += calculate_diff_seconds(charlie_record["time_stamp"],"14:04:41")

ALICE_RECORDS = [
    {'time_stamp': '14:02:03', 'session': 'Start', 'index': 1},
    {'time_stamp': '14:02:34', 'session': 'End'},
    {'time_stamp': '14:02:58', 'session': 'Start'},
    {'time_stamp': '14:03:33', 'session': 'Start'},
    {'time_stamp': '14:03:35', 'session': 'End'},
    {'time_stamp': '14:04:05', 'session': 'End'},
    {'time_stamp': '14:04:23', 'session': 'End'}
]


for idx,alice_record in enumerate(ALICE_RECORDS[:]):
    if alice_record["session"] == "Start" and idx <= len(ALICE_RECORDS):
        adder = (next(end for end in ALICE_RECORDS if end["session"] == "End"))
        user_sessions["alice"]["count"] += 1
        user_sessions["alice"]["seconds"] += calculate_diff_seconds(alice_record["time_stamp"],adder["time_stamp"])
        ALICE_RECORDS.remove(adder)
        ALICE_RECORDS.remove(alice_record)

# print("SO FAR COUNT",user_sessions["alice"]["count"])
# print("SO FAR SECONDS",user_sessions["alice"]["seconds"])

for idx,alice_record in enumerate(ALICE_RECORDS):
    if alice_record["session"] == "End":
        user_sessions["alice"]["count"] += 1
        seconds = calculate_diff_seconds("14:02:03",alice_record["time_stamp"])
        user_sessions["alice"]["seconds"] += seconds
        
    else:
        user_sessions["alice"]["count"] += 1
        user_sessions["alice"]["seconds"] += calculate_diff_seconds(alice_record["time_stamp"],"14:04:41")

# print(validate_line("14 ALICE99 Start"))
# print(validate_line("14:02:05 CHARLIE someMore End"))
# print(validate_line("14:02:34 ALICE99 End"))
# print(validate_line("14:02:58 2 ALICE99 Start"))
# print(validate_line("14:03:02 GG CHARLIE Start"))
# print(validate_line("14:03:33 ALICE99 Bindas"))
# print(validate_line("1403:35 ALICE99 End"))
# print(validate_line("1:3:7:9 CHARLIE End"))


# print(user_sessions)
import sys
FILE_NAME = sys.argv[1]
print(FILE_NAME)