import os

current_dir_path = os.getcwd()  # find paths of the output and input files
reading_file_name = "doctors_aid_inputs.txt"
reading_file_path = os.path.join(current_dir_path, reading_file_name)
writing_file_name = "doctors_aid_outputs.txt"
writing_file_path = os.path.join(current_dir_path, writing_file_name)

if os.path.exists(writing_file_path):  # in order to prevent overwriting the file
    os.remove(writing_file_path)


def read_txtfile():  # read input file line by line and return them
    with open(reading_file_path) as file:
        lines = file.read().splitlines()  # read the lines into a list without \n character
        return lines


def create():  # adds the patient into patient data list
    if split_list in patient_data_list:  # if patient already exist do not add
        output_function(f"Patient {split_list[0]} cannot be recorded due to duplication.")
    else:
        patient_data_list.append(split_list)  # append new patient to patient_data_list
        output_function(f"Patient {split_list[0]} is recorded.")


def remove():  # removes the patient from list if it exists
    if existence is True:  # boolean expression that is returned by line 126
        patient_data_list.pop(place)
        output_function(f"Patient {split_list[0]} is removed.")
    else:  # if there is no such patient
        output_function(f"Patient {split_list[0]} cannot be removed due to absence.")


def list_patients():
    output_function("Patient"+"\t"+"Diagnosis"+"\t"+"Disease"+"\t\t\t"+"Disease"+"\t\t"+"Treatment"+"\t\t"+"Treatment")  # headings
    output_function("Name"+"\t"+"Accuracy"+"\t"+"Name"+"\t\t\t"+"Incidence"+"\t"+"Name"+"\t\t\t"+"Risk" + "\n" + "-"*73)  # headings
    for patient in patient_data_list:
        first_index = float(patient[1])*100  # turns diagnosis accuracy to percentage
        second_index = float(patient[5])*100  # turns treatment risk to percentage
        str_first = f"{first_index:.2f}"+"%"  # turn to a string with 2 decimal places and "%"
        str_second = f"{second_index:.0f}"+"%"  # turn to a string with 0 decimal places and "%"
        if len(patient[0]) < 4:  # sequences of conditions to make the list proper looking and left aligned
            if len(patient[2]) < 12:  # according to lengths of 0,2,4th indexes
                if len(patient[4]) < 8:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t\t\t" + str_second)
                elif len(patient[4]) < 12:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t\t" + str_second)
                elif len(patient[4]) == 16:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + str_second)
                else:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t" + str_second)
            elif len(patient[2]) >= 12:
                if len(patient[4]) < 8:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t\t\t" + str_second)
                elif len(patient[4]) < 12:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t\t" + str_second)
                elif len(patient[4]) == 16:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + str_second)
                else:
                    output_function(patient[0] + "\t\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t" + str_second)
        elif len(patient[0]) >= 4:
            if len(patient[2]) < 12:
                if len(patient[4]) < 8:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t\t\t" + str_second)
                elif len(patient[4]) < 12:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t\t" + str_second)
                elif len(patient[4]) == 16:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + str_second)
                else:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t\t" + patient[3] + "\t" + patient[4] + "\t" + str_second)
            elif len(patient[2]) >= 12:
                if len(patient[4]) < 8:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t\t\t" + str_second)
                elif len(patient[4]) < 12:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t\t" + str_second)
                elif len(patient[4]) == 16:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + str_second)
                else:
                    output_function(patient[0] + "\t" + str_first + "\t\t" + patient[2] + "\t" + patient[3] + "\t" + patient[4] + "\t" + str_second)


def prob_calc():
    if existence is True:  # if patient exists in patient_data_list
        num_den = patient_data_list[place][3].split("/")  # separates disease incident from "/"
        fn = (float(num_den[1]) - float(num_den[0])) * (1 - float(patient_data_list[place][1]))  # amount of people with cancer among cancer-free diagnosed people
        tp = float(num_den[0]) * float(patient_data_list[place][1])  # amount of people who actually has cancer among people diagnosed with cancer
        prob = tp/(fn+tp)*100  # probability of having the disease
        return prob
    else:  # if there is no such patient don't calculate
        return None


def probability():
    if prob_calc() is not None:  # if the prob_calc() function calculated the probability
        if int(prob_calc()) == float(f"{prob_calc():.2f}"):  # if the decimal part is 00... it should print integer
            output_function(f"Patient {patient_data_list[place][0]} has a probability of {prob_calc():.0f}% of having {(patient_data_list[place][2]).lower()}.")
        else:
            output_function(f"Patient {patient_data_list[place][0]} has a probability of {prob_calc():.2f}% of having {(patient_data_list[place][2]).lower()}.")
    else:  # no patient found
        output_function(f"Probability for {split_list[0]} cannot be calculated due to absence.")


def recommendation():
    if existence is True:  # if patient exists
        if prob_calc() > float(patient_data_list[place][5])*100:  # if probability > treatment risk
            output_function(f"System suggests {patient_data_list[place][0]} to have the treatment.")
        elif prob_calc() < float(patient_data_list[place][5])*100:  # if probability < treatment risk
            output_function(f"System suggests {patient_data_list[place][0]} NOT to have the treatment.")
    else:  # if there is no such patient
        output_function(f"Recommendation for {split_list[0]} cannot be calculated due to absence.")


def output_function(out):  # writes args into an output file with "\n"
    with open(writing_file_path, "a") as outfile:
        outfile.write(out)
        outfile.write("\n")


patient_data_list = []  # empty patient data list to append data later

for item in read_txtfile():
    function = item.split(" ", 1)[0]  # separates commands from datas using the space between
    try:
        first_space = item.index(' ')  # locates the space between the command and datas
        split_list = item[first_space + 1:].split(", ")  # splits the datas after space character using ", " characters
    except ValueError:
        split_list = item.split()  # no space character to locate after "list" command
    existence = any(split_list[0] in x for x in patient_data_list)  # returns True if entered name exist on the patient list
    for j in patient_data_list:
        if split_list[0] in j:
            place = patient_data_list.index(j)  # locates the name in multidimensional list
    if function == "create":  # execute functions if they match with the input file commands
        create()
    if function == "remove":  # execute functions if they match with the input file commands
        remove()
    if function == "list":  # execute functions if they match with the input file commands
        list_patients()
    if function == "probability":  # execute functions if they match with the input file commands
        probability()
    if function == "recommendation":  # execute functions if they match with the input file commands
        recommendation()

# Ezgi Ekin
# 2210356029
