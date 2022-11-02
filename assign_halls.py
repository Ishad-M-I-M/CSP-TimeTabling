import argparse
import copy
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def backtracking_search(assiged, proposed_lecture_slots, available_rooms, assigned_rooms={}, d=0):
    if d == len(assiged):
        # assignment complete
        return True

    subject, type, slots = proposed_lecture_slots[d][0], proposed_lecture_slots[d][1], proposed_lecture_slots[d][2:]

    for slot in slots:
        # check whether the slot is already assigned
        if not assigned_rooms.get(slot, False):
            assiged[d] = [subject, slot, available_rooms[0]]
            assigned_rooms[slot] = [available_rooms[0]]

            if backtracking_search(assiged, proposed_lecture_slots, available_rooms, assigned_rooms, d + 1):
                return True
            else:
                assigned_rooms[slot] = []
                assiged[d] = [subject, None, None]
                continue

        if type == "C":
            # consider only the First room since no two lectures can be assigned
            pass
        elif type == "O":
            if len(assigned_rooms.get(slot, [])) > 0:
                already_assigned_rooms = assigned_rooms[slot]
                rooms = copy.deepcopy(already_assigned_rooms)

                if len(already_assigned_rooms) == len(available_rooms):
                    # no remaining rooms
                    continue

                new_room = available_rooms[len(already_assigned_rooms)]
                already_assigned_rooms.append(new_room)

                assiged[d] = [subject, slot, new_room]
                assigned_rooms[slot] = already_assigned_rooms

                if backtracking_search(assiged, proposed_lecture_slots, available_rooms, assigned_rooms, d + 1):
                    return True
                else:
                    assigned_rooms[slot] = rooms
                    assiged[d] = [subject, None, None]

        else:
            raise Exception("Input CSV is not in the requested format")

    else:
        # no assignment succeeded in the loop
        return False


def assign(input_file, output_file):
    with open(input_file) as f:
        data = f.readlines()

    proposed_lecture_slots = [x.strip().split(",") for x in data[:-1]]
    available_rooms = data[-1].strip().split(",")

    # print(*proposed_lecture_slots, sep="\n")
    # print(available_rooms)

    assigned_subjects = []

    for s in proposed_lecture_slots:
        assigned_subjects.append([s[0], None, None])  # initially no timeslot/ room assigned for a subject

    try:
        if not backtracking_search(assigned_subjects, proposed_lecture_slots, available_rooms):
            print(f"{bcolors.WARNING}Cannot Assign Rooms with Given Data{bcolors.ENDC}")

    except Exception as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        sys.exit(-1)

    print(*assigned_subjects, sep="\n")

    with open(output_file, 'w') as f:
        for e in assigned_subjects:
            f.write(",".join(e) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{bcolors.HEADER}{bcolors.UNDERLINE}CSP Time Tabling Problem{bcolors.ENDC}",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('input',
                        metavar=bcolors.OKBLUE + 'input.csv' + bcolors.ENDC,
                        type=str,
                        help="csv file containing raw data.\n"
                             f"* Format of records: {bcolors.OKCYAN}<subject_x>,<compulsory[C]/ optional[O]>{bcolors.ENDC} [one or more time slots]\n"
                             "* Last line available rooms as R1, R2, etc.")

    parser.add_argument('output',
                        metavar=bcolors.OKBLUE + 'output.csv' + bcolors.ENDC,
                        nargs='?',
                        type=str,
                        default="output.csv",
                        help="csv file to write the generated time table.\n"
                             f"Format of entries: {bcolors.OKCYAN}<subject_x>, <time_slot>, <room_assigned>{bcolors.ENDC}")

    args = parser.parse_args()

    assign(args.input, args.output)
