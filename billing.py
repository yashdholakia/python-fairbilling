import sys
from datetime import datetime

user_session_dict = {}
user_session_dict_with_time = {}
master_record = {}

final_session_obj = {}
line_count = 0
user_sessions = {}


def process_file(file_path):
    line_index = 1
    with open(file_path) as file:
        for line in file:
            line = line.rstrip()
            if not validate_line(line):
                continue
            else:
                process_single_line(line, line_index)
                line_index+=1


def process_single_line(line, line_index):
    splitter = line.split()
    time_stamp = splitter[0]
    user_id = splitter[1]
    session = splitter[2]
    master_record[line_index] = {"user_id" : user_id, "time_stamp" : time_stamp, "session" : session}
    
    update_user_session_dict(user_id, session, time_stamp)

    
def update_user_session_dict(user_id, session, time_stamp):
    if user_id not in user_session_dict:
        user_session_dict.update({user_id : [{"time_stamp" : time_stamp, "session" : session }]})
        return user_session_dict

    user_session_dict[user_id].append({"time_stamp" : time_stamp, "session" : session})
    return user_session_dict
    

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
    format = "%H:%M:%S"
    difference = datetime.strptime(end_time, format) - datetime.strptime(start_time, format)
    return int(difference.total_seconds())


def main_executor(file_name):
    
    process_file(file_name)
    if len(user_session_dict) == 0:
        print("No data available")
        sys.exit(-1)

    first_most_record = master_record[1]["time_stamp"]
    last_most_record = master_record[max(master_record.keys())]["time_stamp"]

    for elem in user_session_dict.items():
        user = elem[0]
        session_details = elem[1]
        session_counter = 1
        seconds = 0
        if user not in user_sessions:
            user_sessions.update({ user : { "count" : 0, "seconds" : 0}})

        if len(session_details) > 1:
            for idx,session_record in enumerate(session_details[:]):
                if session_record["session"] == "Start" and (idx) <= len(session_details):
                    try:
                        adder = (next(end for end in session_details if end["session"] == "End"))
                        seconds += calculate_diff_seconds(session_record["time_stamp"],adder["time_stamp"])
                        user_sessions.update({user : {"count" : session_counter, "seconds" : seconds}})
                        session_details.remove(adder)
                        session_details.remove(session_record)
                        session_counter+=1
                    except Exception as e: 
                        continue

        for idx,session_record in enumerate(session_details):
            session_counter = user_sessions[user]["count"]
            old_secs = user_sessions[user]["seconds"]
            if session_record["session"] == "End":
                seconds = calculate_diff_seconds(first_most_record, session_record["time_stamp"])
                seconds = seconds + old_secs
                session_counter+=1
                user_sessions.update({user : {"count" : session_counter, "seconds" : seconds}})
                
            else:
                user_sessions[user]["count"] += 1
                user_sessions[user]["seconds"] += calculate_diff_seconds(session_record["time_stamp"],last_most_record)
                    
            
    for session_info in user_sessions.items():
        print("{} {} {}".format(session_info[0], session_info[1]["count"], session_info[1]["seconds"] ))

if __name__ == "__main__":
    #from CLI parameter
    
    parameters = sys.argv
    if len(parameters) != 2:
        print("Invalid parameters, \n Usage : python3 billing.py <filename>")
        sys.exit(-1)
    
    file_name = parameters[1]
    main_executor(file_name)

   