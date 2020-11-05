import socket
import threading

# class for creating servers


class Server:
    def __init__(self):
        self.SERVER = "127.0.0.1"
        self.PORT = 8080
        self.ADDR = (self.SERVER, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def start(self):
        calendar.struct_calendar()
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print("Active connections", threading.active_count() - 1)

# Class for creating calendars


class Month:
    user_meetings = {}
    calendar_page = []

    def __init__(self):
        self.months = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.months_name = [
            "january", "february", "march", "april",
            "may", "june", "july", "august", "september",
            "october", "november", "december"
            ]
    # add activities to the activity list

    def add_activity(self, activity):
        date = activity.date.split("/")
        month = int(date[0])
        day = int(date[1])
        if str(month) in self.user_meetings:
            if str(day) in self.user_meetings[str(month)]:
                self.user_meetings[str(month)][str(day)].append(activity)
            else:
                self.user_meetings[str(month)][str(day)] = [activity]
        else:
            self.user_meetings[str(month)] = {}
            self.user_meetings[str(month)][str(day)] = [activity]
# get an activity

    def get_activities(self, month, day):
        day = str(day)
        month = str(month)
        stringify = ""
        if month in self.user_meetings:
            if day in self.user_meetings[month]:
                for value in self.user_meetings[month][day]:
                    stringify += f"""
---------------------------------------------------------
By {value.user.username} Date: {value.date}

{value.title}

-----------Description-----------
{value.description}

---------------------------------------------------------\n"""
                return stringify
        stringify = "No meetings on that day"
        return stringify
# fetch a month

    def fetch_month(self, month):
        try:
            month = int(month)
        except ValueError:
            month = str(month)

        if isinstance(month, int):
            if month < 1 or month > 12:
                return False
            else:
                selected_month_name = self.months_name[month-1]
                selected_month = month - 1
        else:
            if month in self.months_name:
                selected_month_name = [i for i in self.months_name if month in i]
                selected_month = self.months_name.index(selected_month_name[0])
            else:
                return False

        month = selected_month
        return month
# struct the calendar

    def struct_calendar(self):

        for i in range(len(self.months)):
            y = []
            y.append(self.months_name[i])
            for j in range(1, self.months[i]+1):
                y.append(j)
            self.calendar_page.append(y)

    def add_calendar_activity(self, date):
        splitted = date.split("/")
        month = int(splitted[0])
        day = int(splitted[1])
        currentMonth = self.calendar_page[month-1]
        for i in currentMonth:
            if i == day:
                currentMonth[i] = "X"

# class for creating activities


class Activity:
    def __init__(self, date, title, description):
        self.date = date
        self.title = title
        self.description = description
        self.user = ""

# class creating new clients


class Client:
    def __init__(self, addr):
        self.username = ""
        self.addr = addr

    def set_username(self, username):
        self.username = username

# creating new calendar by default


calendar = Month()
welcome_message = """
----------------
Welcome to the calendar!

These are the menus you can use

calendar - Open and select a month to see your currently booked meetings
add - Add a new meeting
help - bring up the menu again
exit - Quit application
----------------
"""

# check if day is valid


def check_day(day, month):
    try:
        day = int(day)
        month = int(month)
    except ValueError:
        return False
    check = calendar.months[month]
    if day < 1 or day > check:
        return False
    else:
        return True

# check if date is valid


def check_date(date):
    if "/" in date:
        splittedDate = date.split("/")
        try:
            month = int(splittedDate[0])
            day = int(splittedDate[1])
        except ValueError:
            return False
        if month <= 12 and month >= 1:
            if day <= calendar.months[month-1] and day >= 1:
                return True
        return False
    else:
        return False

# send calendar to client


def send_calendar(calendar):
    stringify = "["
    num = 0
    for i in calendar:
        stringify += f" {i} "
        if num % 7 == 0:
            stringify += "]\n["
        num += 1
    return f"{stringify}]"


def handle_activity(date, title, description, user):
    newActivity = Activity(date.decode(), title, description)
    newActivity.user = user
    calendar.add_activity(newActivity)

# check calendar for activities based on input


def read_calender(conn, calendar):

    conn.send(b'Which month do you want to fetch? Input either a number or by month name')
    data = conn.recv(1024)
    month = calendar.fetch_month(data.decode())
    if month is not False:
        string = send_calendar(calendar.calendar_page[month])

        conn.send(string.encode() + b'\nInput a day you want to check')
        while True:
            day = conn.recv(1024)
            if check_day(day.decode(), month):
                meetings = calendar.get_activities(month+1, day.decode())
                conn.send(meetings.encode())
            else:
                conn.send(b"Returning to main menu")
                break
    else:
        conn.send(b'Input invalid')


def create_user(conn, user):
    conn.send(b'What is your name?')
    data = conn.recv(1024)
    if data:
        user.set_username(data.decode())
        conn.send(b"Welcome user: " + user.username.encode() + welcome_message.encode())


def help_page(conn):
    conn.send(welcome_message.encode())

# create new activity


def create_activity(conn):
    conn.send(b'Which date is the meeting?')
    date = conn.recv(1024)
    if check_date(date.decode()):
        conn.send(b'What is the title of your meeting?')
        title = conn.recv(1024)
        conn.send(b'Give your meeting a description.')
        description = conn.recv(1024)
        return date, title, description
    else:
        conn.send(b"Error not a date")
        return False, False, False

# main menu for each new thread


def handle_client(conn, addr):
    print("New connection")
    connected = True
    user = Client(addr)
    while connected:
        if not user.username:
            create_user(conn, user)
        else:
            data = conn.recv(1024)
            if data:
                print(f"Received string from {user.username}: {data.decode()}")
                # -----Exit application-----
                if (data.decode()).lower() == "exit":
                    connected = False
                elif (data.decode()).lower() == "help":
                    help_page(conn)
                # -----Add new activity-----
                elif (data.decode()).lower() == "add":
                    date, title, description = create_activity(conn)
                    if date is not False:
                        handle_activity(date, title.decode(), description.decode(), user)
                        calendar.add_calendar_activity(date.decode())
                        conn.send(b"New meeting added! \nReturning to main menu.")
                # -----Check the calendar and activities-----
                elif (data.decode()).lower() == "calendar":
                    read_calender(conn, calendar)
                # runs if the command doesn't exist
                else:
                    conn.send(b'Not a command')
            else:
                connected = False
                break

    print(f"{user.username} has disconnected")
    conn.send(b'You have disconnected')
    conn.close()

# starts server and make it listen for new connections


def start_new_server():
    print("Starting server...")
    server = Server()
    server.start()


if __name__ == '__main__':
    start_new_server()
