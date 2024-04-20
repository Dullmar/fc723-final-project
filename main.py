import os

# constants used in the code
ISLE = "X"
STORAGE_AREA = "S"
RESERVED = "R"
FREE = "F"
NUM_ROWS = 7
NUM_COLS = 80
SEATS_FILE = "burak.txt"


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
def book_seat(seats):
    seat_number = input("Enter seat number (e.g 1A): ")
    seat_number = seat_number.strip()
    parsed_seat_number = parse_seat_number(seat_number)
    if parsed_seat_number is None:
        print("That is not a valid seat number.")
    else:
        [row, col] = parsed_seat_number
        if seats[row][col] == FREE:
            seats[row][col] = RESERVED
            print(f"Seat {seat_number} reserved successfully.")
        else:
            print(f"Seat {seat_number} is already reserved.")


# Free a seat
def free_seat(seats):
    seat_number = input("Enter seat number (e.g 1A): ")
    seat_number = seat_number.strip()
    parsed_seat_number = parse_seat_number(seat_number)
    if parsed_seat_number is None:
        print("That is not a valid seat number.")
    else:
        [row, col] = parsed_seat_number
        if seats[row][col] == RESERVED:
            seats[row][col] = FREE
            print(f"Seat {seat_number} freed successfully.")
        else:
            print(f"Seat {seat_number} is not yet reserved.")


# Show the booking state
def show_booking_state(seats):
    letters = ["A", "B", "C", ISLE, "D", "E", "F"]
    i = 0
    j = 0
    booked_seats = []
    for i in range(0, NUM_ROWS):
        for j in range(0, NUM_COLS):
            if seats[i][j] == RESERVED:
                booked_seats.append(f"{j+1}{letters[i]}")
    print(f"Reserved seats({len(booked_seats)}): ", end='')
    print(", ".join(booked_seats))


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


# Write the seat arrangement to a file
def write_seats_to_file(seats):
    with open(SEATS_FILE, "w") as file:
        for row in seats:
            s = ""
            for column in row:
                s += column + " "
            s = s.strip()  # remove extra space at the end
            file.write(s + "\n")


def main():
    print_welcome_message()
    seats = read_seats_from_file()  # get the starting seat arrangement
    user_input = ""
    # loop until the user exits the program by entering 5
    while user_input != "5":
        print_menu()
        user_input = input("Your choice: ").strip()
        if user_input == "1":
            check_seat_availability(seats)
        elif user_input == "2":
            book_seat(seats)
        elif user_input == "3":
            free_seat(seats)
        elif user_input == "4":
            show_booking_state(seats)
        elif user_input == "5":
            pass
        else:
            print("Invalid input. Please try again.")
    pass


main()
