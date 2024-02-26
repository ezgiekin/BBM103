import sys


def output_file(out):  # writes to both terminal and output file
    print(out, end="")
    outfile.write(out)


def create_category():
    if data[i][1] in category:  # checks the category if it exists in dict
        output_file(f"Warning: Cannot create the category for the second time. The stadium has already {data[i][1]}.\n")
    else:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rows_columns = data[i][2].split("x")
        creation = {data[i][1]: {alphabet[j]: ["X" for m in range(int(rows_columns[1]))] for j in range(int(rows_columns[0]))}}
        category.update(creation)  # appending categories(rows as dictionary and columns as list)
        output_file(f"The category '{data[i][1]}' having {int(rows_columns[0])*int(rows_columns[1])} seats has been created\n")


def sell_ticket():
    ticket_category = data[i][3]
    seats = data[i][4:]  # splitting seats from file
    for seat in seats:
        seat_letter = seat[0]  # seat row
        try:
            first, end = seat[1:].split("-")  # seats including range
            seat_range = category[ticket_category][seat_letter][int(first):int(end) + 1]  # wanted seat range
            if int(end) > len(category[ticket_category]["A"]) and (seat_letter not in category[ticket_category]):  # row and column error
                output_file(f"Error: The category '{ticket_category}' has less row and column than the specified index {seat}!\n")
            elif int(end) > len(category[ticket_category]["A"]):  # column error
                output_file(f"Error: The category '{ticket_category}' has less column than the specified index {seat}!\n")
            elif seat_letter not in category[ticket_category]:  # row error
                output_file(f"Error: The category '{ticket_category}' has less row than the specified index {seat}!\n")
            elif ("S" in seat_range) or ("F" in seat_range) or ("T" in seat_range):  # already taken seats
                output_file(f"Warning: The seats {seat} cannot be sold to {data[i][1]} due some of them have already been sold!\n")
            else:  # if there's no error sell seats
                for j in range(int(first), int(end)+1):
                    if data[i][2] == "student":
                        category[ticket_category][seat_letter][j] = "S"
                    elif data[i][2] == "full":
                        category[ticket_category][seat_letter][j] = "F"
                    elif data[i][2] == "season":
                        category[ticket_category][seat_letter][j] = "T"
                output_file(f"Success: {data[i][1]} has bought {seat} at {ticket_category}\n")
        except ValueError:
            seat_num = seat[1:]  # individual seats
            individual = category[ticket_category][seat_letter][int(seat_num)]
            if int(seat_num) > len(category[ticket_category]["A"]) and seat_letter not in category[ticket_category]:  # row and column error
                output_file(f"Error: The category '{ticket_category}' has less row and column than the specified index {seat}!\n")
            elif int(seat_num) > len(category[ticket_category]["A"]):  # column error
                output_file(f"Error: The category '{ticket_category}' has less column than the specified index {seat}!\n")
            elif seat_letter not in category[ticket_category]:  # row error
                output_file(f"Error: The category '{ticket_category}' has less row than the specified index {seat}!\n")
            elif ("T" == individual) or ("S" == individual) or ("F" == individual):  # already taken seats
                output_file(f"Warning: The seat {seat} cannot be sold to {data[i][1]} since it was already sold!\n")
            else:  # if there's no error sell seats
                if data[i][2] == "student":
                    category[ticket_category][seat_letter][int(seat_num)] = "S"
                elif data[i][2] == "full":
                    category[ticket_category][seat_letter][int(seat_num)] = "F"
                elif data[i][2] == "season":
                    category[ticket_category][seat_letter][int(seat_num)] = "T"
                output_file(f"Success: {data[i][1]} has bought {seat} at {ticket_category}\n")


def cancel_ticket():
    ticket_category = data[i][1]
    seats = data[i][2:]  # seats to be canceled
    for seat in seats:
        seat_letter = seat[0]
        seat_num = int(seat[1:])
        if int(seat_num) > len(category[ticket_category]["A"]) and seat_letter not in category[ticket_category]:
            output_file(f"Error: The category '{ticket_category}' has less row and column than the specified index {seat}!\n")
        elif int(seat_num) > len(category[ticket_category]["A"]):
            output_file(f"Error: The category '{ticket_category}' has less column than the specified index {seat}!\n")
        elif seat_letter not in category[ticket_category]:
            output_file(f"Error: The category '{ticket_category}' has less row than the specified index {seat}!\n")
        elif category[ticket_category][seat_letter][seat_num] == "X":  # empty seat error
            output_file(f"Error: The seat {seat} at '{ticket_category}' has already been free! Nothing to cancel\n")
        else:  # if there's ne error cancel seat
            category[ticket_category][seat_letter][seat_num] = "X"
            output_file(f"Success: The seat {seat} at {ticket_category} has been canceled and now ready to sell again\n")


def balance():
    f_sum = sum(1 if value == "F" else 0 for x in category[data[i][1]].values() for value in x)  # number of full
    s_sum = sum(1 if value == "S" else 0 for x in category[data[i][1]].values() for value in x)  # number of students
    t_sum = sum(1 if value == "T" else 0 for x in category[data[i][1]].values() for value in x)  # number of seasons
    revenues = s_sum*10 + f_sum*20 + t_sum*250  # total money
    output_file(f"Category report of '{data[i][1]}'\n"+"-"*32+"\n")
    output_file(f"Sum of students = {s_sum}, Sum of full pay = {f_sum}, Sum of season ticket = {t_sum}, and Revenues = {revenues} Dollars\n")


def show_category():
    output_file(f"Printing category layout of {data[i][1]}\n\n")
    res = dict(reversed(list(category[data[i][1]].items())))  # reversed dict items
    for key, value in res.items():
        output_file(f"{key} "+"  ".join(value)+"\n")  # printing category layout
    for m in range(len(res.values())):
        output_file(f"{m}".rjust(3))  # column numbers
    output_file("\n")


with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    data = [[data for data in item.split(" ")] for item in lines]  # appending every line in file to a list
category = {}
outfile = open("output.txt", "w")  # opening an output file
for i in range(len(lines)):  # executing commands
    if "CREATECATEGORY" in data[i]:
        create_category()
    elif "SELLTICKET" in data[i]:
        sell_ticket()
    elif "CANCELTICKET" in data[i]:
        cancel_ticket()
    elif "BALANCE" in data[i]:
        balance()
    elif "SHOWCATEGORY" in data[i]:
        show_category()
outfile.close()

# Ezgi EKİN
# 2210356029
