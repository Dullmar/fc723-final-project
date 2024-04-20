import os
import random

# constants used in the code
ISLE = "X"
STORAGE_AREA = "S"
RESERVED = "R"
FREE = "F"
NUM_ROWS = 7
NUM_COLS = 80
SEATS_FILE = "burak.txt"
CUSTOMERS_FILE = "customers.txt"


# print the menu options
def print_menu():
    print("1. Check availability of seat")
    print("2. Book a seat.")
    print("3. Free a seat.")
    print("4. Show booking state.")
    print("5. Exit program.")


def print_welcome_message():
    print("*********************************")
    print("Welcome to Apache Airlines")
    print("*********************************")


# Check if a seat is available
def check_seat_availability(seats):
    seat_number = input("Enter seat number (e.g 1A): ")
    seat_number = seat_number.strip()
    parsed_seat_number = parse_seat_number(seat_number)
    if parsed_seat_number is None:
        print("That is not a valid seat number.")
        return False
    [row, col] = parsed_seat_number
    seat = seats[row][col]
    if seat == FREE:
        print(f"Seat {seat_number} is available.")
        return True
    else:
        print(f"Seat {seat_number} is reserved.")
        return False


# parses a seat number, e.g 1A or 89A and returns the row and column, or None if
# the seat number is not valid
def parse_seat_number(seat_number):
    seat_number = seat_number.strip()
    # the last character is a letter, then the first one or two characters are a number
    if len(seat_number) < 2 or len(seat_number) > 3:
        return None
    row_letter = seat_number[len(seat_number) - 1]
    row_letter = row_letter.upper()
    letters = ["A", "B", "C", "D", "E", "F"]
    if row_letter in letters:
        row = letters.index(row_letter)
        # the isle is row number 3, so if row is after C, add 1
        if row > 2:
            row += 1
    else:
        # the row is not valid
        return None
    column_digits = seat_number[0 : len(seat_number) - 1]
    if column_digits.isnumeric():
        column = int(column_digits) - 1  # the list uses zero-based indexing
        # the column must be between 0 and NUM_COLS - 1
        if column < 0 or column >= NUM_COLS:
            # out of valid range
            return None
    else:
        # the column is not valid
        return None

    # column 77 and 76 are storage area for rows 4, 5, and 6
    if (column == 77 or column == 76) and row in [4, 5, 6]:
        # seat is storage area
        return None

    return [row, column]


# Book a seat
def book_seat(seats, customers):
    seat_number = input("Enter seat number (e.g 1A): ")
    seat_number = seat_number.strip()
    seat_number = seat_number.upper()
    parsed_seat_number = parse_seat_number(seat_number)
    if parsed_seat_number is None:
        print("That is not a valid seat number.")
    else:
        [row, col] = parsed_seat_number
        if seats[row][col] == FREE:
            # get customer information
            customer_name = input("Enter customer name: ").strip()
            passport_number = input("Enter customer passport number: ").strip()
            # generate a reference number
            reference_number = generate_reference_number(seats)
            customers.append(
                {
                    "reference_number": reference_number,
                    "customer_name": customer_name,
                    "passport_number": passport_number,
                    "seat_number": seat_number,
                }
            )
            seats[row][col] = RESERVED
            print(f"Seat {seat_number} reserved successfully.")
        else:
            print(f"Seat {seat_number} is already reserved.")


# Free a seat
def free_seat(seats, customers):
    seat_number = input("Enter seat number (e.g 1A): ")
    seat_number = seat_number.strip()
    seat_number = seat_number.upper()
    parsed_seat_number = parse_seat_number(seat_number)
    if parsed_seat_number is None:
        print("That is not a valid seat number.")
    else:
        [row, col] = parsed_seat_number
        if seats[row][col] == RESERVED:
            # remove the seat number and reference from the customers list
            new_customers = [c for c in customers if c["seat_number"] != seat_number]
            customers = new_customers[:]
            seats[row][col] = FREE
            print(f"Seat {seat_number} freed successfully.")
        else:
            print(f"Seat {seat_number} is not yet reserved.")


# Show the booking state
def show_booking_state(seats, customers):
    letters = ["A", "B", "C", ISLE, "D", "E", "F"]
    i = 0
    j = 0
    booked_seats = []
    for i in range(0, NUM_ROWS):
        for j in range(0, NUM_COLS):
            if seats[i][j] == RESERVED:
                booked_seats.append(f"{j+1}{letters[i]}")
    print(f"Reserved seats({len(booked_seats)}): ")
    for seat in booked_seats:
        customer = get_customer_seat(seat, customers)
        print(f"Seat {seat}: {customer['customer_name']}")


# Read the seat arrangement from a file
def read_seats_from_file():
    seats = []  # the seats are stored in a two dimensional array
    # the plane is size 80 x 7 but the middle row is the isle
    # columns 77 and 78 of the last three rows are the storage area

    # assume a seat is free unless it is explictly reserved in the file
    for i in range(0, NUM_ROWS):
        row = []
        for j in range(0, NUM_COLS):
            if i == 3:
                row.append(ISLE)  # row 3 is the isle
            elif i >= 4 and (j == 77 or j == 76):  # storage area
                row.append(STORAGE_AREA)
            else:
                row.append(FREE)
        seats.append(row)

    # check if there are any reservations from the file
    if os.path.exists(
        SEATS_FILE
    ):  # the file might not exist (the very first time that the program is run)
        with open(SEATS_FILE, "r") as file:
            lines = file.readlines()
            row = 0
            for line in lines:
                line = line.strip()
                # ignore blank lines
                if len(line) == 0:
                    continue
                col = 0
                for seat in line.split(" "):
                    seats[row][col] = seat
                    col += 1
                row += 1

    return seats


# read the customer information and reference numbers from the file
def read_customers_from_file():
    customers = []  # use a list where each element is a dictionary
    # the file is written in the following format (the dictionary will also have the same keys):
    # reference_number
    # customer_name
    # passport_number
    # seat_number
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                reference_number = lines[i].strip()
                customer_name = lines[i + 1].strip()
                passport_number = lines[i + 2].strip()
                seat_number = lines[i + 3].strip()
                customers.append(
                    {
                        "reference_number": reference_number,
                        "customer_name": customer_name,
                        "passport_number": passport_number,
                        "seat_number": seat_number,
                    }
                )
    return customers


# write the customer information and reference numbers to file
def write_customers_to_file(customers):
    with open(CUSTOMERS_FILE, "w") as file:
        for customer in customers:
            file.write(customer["reference_number"] + "\n")
            file.write(customer["customer_name"] + "\n")
            file.write(customer["passport_number"] + "\n")
            file.write(customer["seat_number"] + "\n")


# get the customer who reserved a seat. Returns None if no such seat has been reserved.
def get_customer_seat(seat_number, customers):
    for c in customers:
        if c["seat_number"] == seat_number:
            return c
    return None


# Write the seat arrangement to a file
def write_seats_to_file(seats):
    with open(SEATS_FILE, "w") as file:
        for row in seats:
            s = ""
            for column in row:
                s += column + " "
            s = s.strip()  # remove extra space at the end
            file.write(s + "\n")


# check whether a reference number is unique
def is_unique_reference_number(seats, reference_number):
    for row in seats:
        for column in row:
            if column == reference_number:
                return False
    return True


# generate a reference number (8 alphanumeric characters)
def generate_reference_number(seats):
    # pick 4 random numbers and 4 random letters, then shuffle them
    # to get a reference number. This process is repeated until
    # we get a unique reference number

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "u",
        "w",
        "x",
        "y",
        "z",
    ]

    random_numbers = random.sample(numbers, 4)
    random_letters = random.sample(letters, 4)
    random_numbers_and_letters = random_letters + random_numbers
    random.shuffle(random_numbers_and_letters)
    reference_number = "".join(random_numbers_and_letters)
    while not is_unique_reference_number(
        seats, reference_number
    ):  # this loop is guaranteed to not be infinite because there are so many ways to choose numbers and letters
        random_numbers = random.choice(numbers)
        random_letters = random.choice(letters)
        random_numbers_and_letters = random_letters + random_numbers
        random.shuffle(random_numbers_and_letters)
        reference_number = "".join(random_numbers_and_letters)

    return reference_number


def main():

    print_welcome_message()
    seats = read_seats_from_file()  # get the starting seat arrangement
    customers = read_customers_from_file()
    user_input = ""
    # loop until the user exits the program by entering 5
    while user_input != "5":
        print_menu()
        user_input = input("Your choice: ").strip()
        if user_input == "1":
            check_seat_availability(seats)
        elif user_input == "2":
            book_seat(seats, customers)
        elif user_input == "3":
            free_seat(seats, customers)
        elif user_input == "4":
            show_booking_state(seats, customers)
        elif user_input == "5":
            pass
        else:
            print("Invalid input. Please try again.")
    write_seats_to_file(seats)
    write_customers_to_file(customers)


main()
