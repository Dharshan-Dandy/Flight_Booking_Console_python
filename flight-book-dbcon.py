import sqlite3
import re
from prettytable import PrettyTable
import datetime

class DB_connect:
    def __init__(self):  # constructor
        # database name of flight booking Name
        try:
            db_name = "flight-DB-python"
            self.connect = sqlite3.connect(db_name)
            self.cursor = self.connect.cursor()
                
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_credential (email TEXT PRIMARY KEY,name TEXT,passwd TEXT,dob DATE,
            type INTEGER)''')

            self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS flight_data (
        flight_no TEXT PRIMARY KEY,
        flight_type TEXT,
        Destination TEXT,
        Dest_time TIMESTAMP,
        Arrival TEXT,
        Arr_time TIMESTAMP,
        nOfseats INTEGER,
        Status TEXT
    )''')

            self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS booktory_data (
        flight_no TEXT,
        cust_email_name TEXT,
        booked_date TIMESTAMP,
        FOREIGN KEY (flight_no) REFERENCES flight_data(flight_no)
    )''')

                                

            self.connect.commit()
        except sqlite3.Error as Err:
            self.connect.rollback()
            print("Database Error : ", Err)


# Admin Work Space
class Admin(DB_connect):
    def __init__(self,user_data):
        super().__init__()
        self.user_data = user_data


    def get_flight_data(self, status):
        self.cursor.execute("SELECT * FROM flight_data WHERE Status IN (?, ?)", (status[0],status[1]))
        fetched_data = self.cursor.fetchall()

        if not fetched_data:
            print(f"No Information about {status[0]} Flights!!")
        else:
            avail_table = PrettyTable(["Flight_No", "Flight_Type", 'Departure Airport', 'Date Time', 'Arrival Airport', 'Date_Time', 'No_of_Seats', 'Status'])
            avail_table.add_rows(fetched_data)
            print(f"{status[0]} Flight Data:")
            print(avail_table)

    def addFlight(self,flight_add_details):
                    try:
                        self.cursor.execute("INSERT INTO flight_data VALUES(?, ?, ?, ?, ?, ?, ?, ?)",(flight_add_details[0],flight_add_details[1],flight_add_details[2],flight_add_details[3],flight_add_details[4],flight_add_details[5],flight_add_details[6],flight_add_details[7]))
                        self.connect.commit()
                    except sqlite3.Error as err:
                        self.connect.rollback()
                        print("Inserting Error",err)
                    print("\nAdding",flight_add_details[0],"Successfully Done..\n")



    def modifyFlight(self,flight_add_details):

            try:
                self.cursor.execute("UPDATE flight_data SET flight_type = ?, Destination = ?, Dest_time = ?, Arrival = ?, Arr_time = ?, nOfseats = ?, Status = ? WHERE flight_no = ?", (flight_add_details[1], flight_add_details[2], flight_add_details[3], flight_add_details[4], flight_add_details[5], flight_add_details[6], flight_add_details[7], flight_add_details[0]))
                self.connect.commit()


                print("Modified Done")
            except sqlite3.Error as err:
                self.connect.rollback()
                print("Updating Error:", err)


    def viewFlight(self):
         #Availabe Flight Data:
         self.get_flight_data(("Available",'Yes'))
            
         #Not Avilable Data
         self.get_flight_data(("Not Available","No"))
        

         #Other Data
         self.get_flight_data(('Other',''))
    

    def find_flight(self,flight_no):
        self.cursor.execute("select count(*) from flight_data where flight_no = ?",(flight_no,))
        
        if self.cursor.fetchall()[0][0] == 0 :
            return False
        else:
            return True
    
    def delete_flight(self,flight_no):
        try:
            self.cursor.execute("DELETE FROM flight_data WHERE flight_no = ?",(flight_no,))
            self.connect.commit()
            return True
        except sqlite3.Error as err: 
            print("Deleting Error",err)
            self.connect.rollback()
            return False
        
    def view_booktory(self):
        self.cursor.execute("SELECT * FROM booktory_data")
        fetched_data = self.cursor.fetchall()

        if not fetched_data:
            print(f"No Information ")
        else:
            avail_table = PrettyTable(["Flight_No",'user_data','Booked_time'])
            avail_table.add_rows(fetched_data)
            print(f"Book History Data:")
            print(avail_table)






# User Work Space
class User(DB_connect):
    def __init__(self,user_data):
        super().__init__()
        self.user_data = user_data


    def check_flight(self,flight_no):
        self.cursor.execute("SELECT COUNT(*) FROM flight_data WHERE flight_no = ? and Status in (?, ?)",(flight_no,"Yes","Available"))
        if self.cursor.fetchall()[0][0] == 1:
            return True
        else:
            return False

    def book_flight(self,flight_no):
        if self.check_flight(flight_no) :

            try:
               self.cursor.execute("INSERT INTO booktory_data VALUES (?, ?, ?)",(flight_no," ".join([self.user_data[-1],self.user_data[0]]),datetime.datetime.now()))
               self.connect.commit()
               print(f"Flight {flight_no} Booked Successfully")
            except sqlite3.Error as err:
                self.connect.rollback()
                print('DB Error : ',err)
        else:
            print(f"Sorry the Flight {flight_no} Not Available")

    def booktory(self):
        self.cursor.execute("SELECT * FROM booktory_data WHERE cust_email_name = ?",(' '.join([self.user_data[-1],self.user_data[0]]),))
        fetched_data = self.cursor.fetchall()

        if not fetched_data:
            print(f"No Book History")
        else:
            avail_table = PrettyTable(["Flight_No",'user_data','Booked_time'])
            avail_table.add_rows(fetched_data)
            print(f"Book History Data:")
            print(avail_table)


            



class FlightbookApp(Admin,User):
    def __init__(self,user_data):
        #super().__init__(user_data)
        self.user_data = user_data
        #print(self.user_data)




    def get_flight_data(self, status):
        DB = DB_connect()
        DB.cursor.execute("SELECT * FROM flight_data WHERE Status IN (?, ?)", (status[0],status[1]))
        fetched_data = DB.cursor.fetchall()

        if not fetched_data:
            print(f"No Information about {status[0]} Flights!!")
        else:
            avail_table = PrettyTable(["Flight_No", "Flight_Type", 'Departure Airport', 'Date Time', 'Arrival Airport', 'Date_Time', 'No_of_Seats', 'Status'])
            avail_table.add_rows(fetched_data)
            print(f"{status[0]} Flight Data:")
            print(avail_table)


    def find_flight(self,flight_no):
        DB = DB_connect()
        DB.cursor.execute("select count(*) from flight_data where flight_no = ?",(flight_no,))

        if DB.cursor.fetchall()[0][0] == 0 :
            return False
        else:
            return True


    def viewFlight(self):
         #Availabe Flight Data:
         self.get_flight_data(("Available",'Yes'))

         #Not Avilable Data
         self.get_flight_data(("Not Available","No"))

         #Other Data
         self.get_flight_data(('Other',''))




    def workSpace(self):
        if self.user_data[1] == 1 :
            admin = Admin(self.user_data)
            while True:
                choice = input('> View\n> Add \n> Edit\n> Delete\n> Booktory\n> Quit\n>> ')
                if choice == 'Add':
                    print("Enter Information of Flight")
                    flight_add_details = []
                    flight_add_details.append(input("FlightNo > "))
                    flight_add_details.append(input("FlightType > "))
                    flight_add_details.append(input("Departure Airport > "))
                    flight_add_details.append(input("Dest_Date > "))
                    flight_add_details[-1]=(' '.join([flight_add_details[-1],input("Dest_Time > ")]))
                    flight_add_details.append(input("Arrival Airport > "))
                    flight_add_details.append(input("Arrival_Date > "))
                    flight_add_details[-1]=(' '.join([flight_add_details[-1],input("Arrival_Time > ")]))
                    flight_add_details.append(input("No_Of_Seats > "))
                    flight_add_details.append(input("Status > "))
                    admin.addFlight(flight_add_details)
                elif choice == 'View':
                     self.viewFlight()

                elif choice == 'Quit' :
                    break
                
                elif choice == "Delete" :
                    self.viewFlight()
                    flag_available = True
                    while flag_available :
                        flight_no = input("Enter Flight Number > ")
                        response = self.find_flight(flight_no)
                        if response :
                            print("Confirmation Delete",flight_no," [Y/N] > ",end='') 
                            choice = input()
                            if choice == 'Y':
                                if  admin.delete_flight(flight_no):
                                    print("Flight",flight_no,"Successfully Deleted !")
                                    break
                                else:
                                    print("Sorry Internal Error")
                            else:
                                break
                        else :

                            print("Flight No is not Register\nTry Again ")
                            break
                elif choice == 'Edit' : 
                    self.viewFlight()
                    flight_no = input("Enter Flight Number > ")
                    if self.find_flight(flight_no):
                        print("Enter New  Information of Flight")
                        flight_add_details = [flight_no]
                        #flight_add_details.append(input("FlightNo > "))
                        flight_add_details.append(input("FlightType > "))
                        flight_add_details.append(input("Departure Airport > "))
                        flight_add_details.append(input("Dest_Date > "))
                        flight_add_details[-1]=(' '.join([flight_add_details[-1],input("Dest_Time > ")]))
                        flight_add_details.append(input("Arrival Airport > "))
                        flight_add_details.append(input("Arrival_Date > "))
                        flight_add_details[-1]=(' '.join([flight_add_details[-1],input("Arrival_Time > ")]))
                        flight_add_details.append(input("No_Of_Seats > "))
                        flight_add_details.append(input("Status > "))
                        admin.modifyFlight(flight_add_details)
                    else:
                        print("Flight Number Not Available")
                elif choice == 'Booktory':
                    admin.view_booktory()

        
        elif self.user_data[1]==2 :
            user = User(self.user_data)
            while True:
                user_choice = input("> View\n> Book\n> Booktory\n> Quit\n> ")
                if user_choice == "Booktory" :
                    user.booktory()
                elif user_choice == "View" :
                    self.viewFlight()
                elif user_choice == "Book":
                    book_flight_no = input("Enter Flight No > ")
                    if not self.find_flight(book_flight_no):
                        print("Flight Number Invalid !!")
                        continue
                    else:
                        user.book_flight(book_flight_no)
                        continue
                elif user_choice == 'Quit':
                    break




class Login_module(DB_connect):
    def __init__(self):
        super().__init__()

    @staticmethod
    def encrypt(text, key):
        return ''.join([chr(ord(char) ^ key) for char in text])

    def validate_date(self, dob):
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not bool(re.match(date_pattern, dob)):
            return False
        else:
            year = int(dob[0:4])
            mon = int(dob[5:7])
            date = int(dob[8::])
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                if mon == 2:
                    return True if 29 >= date > 0 else False
            else:
                if mon == 2:
                    return True if 28 >= date > 0 else False
            if mon % 2 == 0:
                if 7 > mon > 0 and 0 < date < 31:
                    return True
                elif 13 > mon > 7 and 0 < date <= 31:
                    return True
            else:
                if 0 < mon <= 7 and 0 < date <= 31:
                    return True
                elif 13 > mon > 8 and 0 < date < 31:
                    return True
            return False

    @property
    def signup(self):

        details = []
        interrupt = False
        print("Enter 0 Anywhere to Exit")
        while True and not interrupt:
            u_name = input("Enter UserName >> ")
            if u_name == '0':
                interrupt = True
            else:
                details.append(u_name)
                break

        while True and not interrupt:
            email = input("Enter Email >> ")
            if email == 0:
                interrupt = True
                break
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if re.match(email_regex, email):
                try:
                    self.cursor.execute('SELECT count(*) FROM user_credential WHERE email = ? ', (email,))
                except sqlite3.Error as error:
                    self.connect.rollback()
                    print("Database Error : ", error)
                    interrupt = True

                info = self.cursor.fetchall()
                # print(info)
                if not info[0][0]:
                    details.append(email)
                else:
                    print("Email Already Registered !")
                    continue
                break
            else:
                print("Not Valid Email")
        while True and not interrupt:
            pas_wd = input("Enter PassWord >> ")
            pas_wd.strip()
            if pas_wd == '0':
                interrupt = True
                break
            pwd_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

            match = re.match(pwd_pattern, pas_wd)

            if match and details[0] != pas_wd:
                details.append(pas_wd)
                break
            else:
                print("Invalid Password,Try another")
        while True and not interrupt:
            dob = input("Enter DOB: yyyy-MM-dd >> ")
            if dob == '0':
                interrupt = True
                break

            if self.validate_date(dob):
                details.append(dob)
                break
            else:
                print("Not Valid Date")
        while True and not interrupt:
            u_a = input("Enter 1 for Admin (or) 2 for User >> ")
            if u_a == '0':
                interrupt = True
                break
            if u_a == '1':
                details.append(1)
                break
            elif u_a == '2':
                details.append(2)
                break
            else:
                continue

                # Now insert or create the record in the table
        if not interrupt:

            details[2] = self.encrypt(details[2], len(details[2]))
            # details = [ username , email ,password, dob, admin/user ]
            # table = mail TEXT,name TEXT,passwd TEXT,dob DATE, type INTEGER
            try:
                self.cursor.execute("INSERT INTO user_credential VALUES (?, ?, ?, ?, ?)",
                                    (details[1], details[0], details[2], details[3], details[4]))
                self.connect.commit()
                return True
            except sqlite3.Error as error:
                self.connect.rollback()
                print("Database Error :", error)
                print("DB_connection is failed please refer in Internet")
                return False
        else:
            return False

    def login(self):
        print("Enter 0 Anywhere to Exit")
        pwd_changed = False
        forgot_pwd_flag = False
        while True:

            given_email = input("Enter Email Id >> ")
            if given_email == '0':
                return -1
            else:
                given_pwd = input("Enter Password >> ")
                try:
                    self.cursor.execute("select count(*),passwd,name,type,email from user_credential where email = ?",
                                        (given_email,))
                except sqlite3.Error as err:
                    print("Database Error on find User : ", err)
                    return -1
                info_query = self.cursor.fetchall()
                if info_query[0][0] == 0:
                    print("User Not Found!")
                    continue
                if self.encrypt(given_pwd, len(given_pwd)) == info_query[0][1]:
                    return info_query[0][2::]
                else:
                    change_pwd_choice = input("Invalid Password!\nDue Want to Reset Password Press 0 else 1 >> ")
                    if change_pwd_choice == '1':
                        continue
                    if change_pwd_choice == '0':
                        while True:
                            new_pwd = input("Enter New Password >> ")
                            pwd_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

                            if bool(re.match(pwd_pattern, new_pwd)):
                                try:
                                    self.cursor.execute(
                                        "UPDATE user_credential SET passwd = ? where email = ?",
                                        (self.encrypt(new_pwd, len(new_pwd)), given_email)
                                    )
                                    self.connect.commit()
                                    print("Password Changed !")
                                    break
                                except sqlite3.Error as err:
                                    self.connect.rollback()
                                    print("DB Error : ", err)
                            else :
                                print("Invalid Password, Try Again ")
                                continue


if __name__ == "__main__":

    print('''#--------------------------------------------------
#--------------FLIGHT BOOKING SYSTEM--------------
#__________________________________________________''')
    while True:
        user_choice = int(input("Hi, Choose :\nSign Up : 1 (or) Sign In : 2 >> "))
        login = Login_module()
        if user_choice == 1:
            if login.signup:
                print("Successfully Sign Up")
            else:
                print("Please Try again")
                continue
        if user_choice == 2:
            user_details = login.login()
            if user_details == -1:
               continue
            FlightAPP = FlightbookApp(user_details)
            FlightAPP.workSpace()


