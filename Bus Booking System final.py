#function for connecting to mysql.
def dbconnect(h,u,p):
    import mysql.connector as ms
    try:
        conn=ms.connect(host=h,user=u,passwd=p)
        print("Connected to mysql...")
        return conn
    except:
        print("Connection failed...")
        return False

#function for intialisation.
def init(dbname,conn):
    cur=conn.cursor()
    sql='show databases;'
    cur.execute(sql)
    result=cur.fetchall()
    for row in result:
        if row[0]==dbname:
            print("Database Found")
            sql='use {}'.format(dbname)
            cur.execute(sql)
            cur.close()
            break
    else:
        print("Database not found.")
        print("Creating database and tables...")
        sql='create database {}'.format(dbname)
        cur.execute(sql)
        sql='use {}'.format(dbname)
        cur.execute(sql)

        #Buses
        sql='create table buses(bus_id INT PRIMARY KEY AUTO_INCREMENT,bus_from varchar(40),bus_to varchar(40),start_time time,journey_time time, arival_time time, fare int)'
        cur.execute(sql)
        #Users
        sql='create table users(user_id INT PRIMARY KEY AUTO_INCREMENT,name varchar(40) ,email varchar(40) UNIQUE ,password varchar(8))'
        cur.execute(sql)
        #creating admin user
        sql='insert into users values(1,"admin","admin@gmail","admin")'
        cur.execute(sql)
        #Bookings
        sql='create table bookings(booking_id INT PRIMARY KEY AUTO_INCREMENT, user_id int, bus_id int, journey_date date,seat int)'
        cur.execute(sql)
        #stats
        sql='create table stats(bus_id int,journey_date date, availability int)'
        cur.execute(sql)

        print("Database created Successfully...")
        cur.close()

def signin(conn):
    print('\nLogin to your account...')
    cur = conn.cursor()
    email = input("Enter email : ")
    passwd = input("Enter password : ")
    sql = 'select * from users where email="{}" and password="{}"'.format(email,passwd)
    cur.execute(sql)
    res = cur.fetchone()
    
    n = cur.rowcount
    
    if n == 0:
        cur.close()
        print("LOGIN FAILED! Invalid email or password.")
        return 0,0
    else:
        print("LOGIN SUCCESSFUL.")
        uid, uname = res[0],res[1]
        cur.close()
        return uid,uname
    
def register(conn):
    cur = conn.cursor()
    name = input("Enter name: ")
    email = input("Enter email : ")
    passwd = input("Enter password : ")
    sql = 'insert into users(name,email,password) values("{}","{}","{}")'.format(name,email,passwd)
    try:
        cur.execute(sql)
        print("User registration successful")
        cur.close()
        return True
    except:
        cur.close()
        print("Email already exists.")
        return False

def admin(conn):
    menu='''
    1. View booking for a bus
    2. Create a new bus route
    3. Delete a bus route
    4. View bookings on all routes for a date
    5. View bus routes
    6. Sign out
    '''

    while True:
        print(menu)
        ch = int(input("Enter your choice : "))
        if ch==1:
            cur = conn.cursor()
            b_id = int(input("Enter bus id : "))
            sql = 'select u.user_id,name,email,bus_id,journey_date,seat from bookings b, users u where b.user_id = u.user_id and b.bus_id={};'.format(b_id)
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format('UID', 'Passenger Name', 'Email', 'BUSID', 'Date', 'Seat'))
            if len(res)==0:
                print("No booking found.")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format(row[0], row[1], row[2],row[3],str(row[4]),row[5]))
            cur.close()
        elif ch==2:
            cur = conn.cursor()
            bus_id=int(input("Enter Bus Id: "))
            from_bus =input("From: ")
            to_bus=input("To: ")
            s=input("Start time (hh:mm): ")
            j=input("Journey  time (hh:mm): ")
            a=input("Arrival time (hh:mm): ")
            fare=int(input("Enter Fare: "))
            sql = 'insert into buses values({},"{}","{}","{}","{}","{}",{})'.format(bus_id,from_bus,to_bus,s,j,a,fare)
            cur.execute(sql)
            print("Route Added.")
            cur.close()
            
        elif ch==3:
            cur = conn.cursor()
            b_id = int(input("Enter bus id : "))
            sql='delete from buses where bus_id={};'.format(b_id)
            cur.execute(sql)
            print("Route Deleted.")
            cur.close()
        elif ch==4:
            cur=conn.cursor()
            
            d= input("Enter Date (YYYY-MM-DD) : ")
            sql = 'select u.user_id,name,email,bus_id,journey_date,seat from bookings b, users u where b.user_id = u.user_id and b.journey_date="{}";'.format(d)
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format('UID', 'Passenger Name', 'Email', 'BUSID', 'Date', 'Seat'))
            if len(res)==0:
                print("No bookings found.")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<30}{:<7}{:<12}{:>7}'.format(row[0], row[1], row[2],row[3],str(row[4]),row[5]))
            cur.close()
            
        elif ch==5:
            
            cur=conn.cursor()

            
            sql = 'select * from buses ;'
            cur.execute(sql)
            res = cur.fetchall()
            print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format('BID', 'From', 'To', 'Start Time', 'Journey Time', 'Arrival Time','Fare'))
            if len(res)==0:
                print("No bookings found.")
            else:
                for row in res:
                    print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format(row[0], row[1], row[2],str(row[3]),str(row[4]),str(row[5]),row[6]))
            cur.close()
        elif ch==6:
            print("\nSigned Out...")
            break
        else:
            print("INVALID CHOICE")

def user(uid, uname, conn):
    menu='''

    1. Book a ticket
    2. View your bookings
    3. Cancel your ticket
    4. Sign out
    '''

    while True:
        print(menu)
        ch=int(input("Enter your choice: "))
        if ch==1:
            cur=conn.cursor()
            f=input("From : ")
            t=input("To : ")
            sql = 'select * from buses where bus_from="{}" and bus_to = "{}"'.format(f,t)
            cur.execute(sql)
            res = cur.fetchall()
            if cur.rowcount==0:
                print("Sorry! No buses found on this route")
            else:
                d = input("Date(YYYY_MM_DD) : ")
                msg = "Following buses are found on this route"
                print(msg)
                print('-'*len(msg))
                print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format('BID', 'From', 'To', 'Start Time', 'Journey Time', 'Arrival Time','Fare'))
                for row in res:
                    print('{:<5}{:<20}{:<20}{:<15}{:<15}{:<15}{:>6}'.format(row[0], row[1], row[2],str(row[3]),str(row[4]),str(row[5]),row[6]))

                u_b_id = int(input("Enter bus id to book ticket : "))
                sql = 'Select * from stats where bus_id={} and journey_date="{}"'.format(u_b_id, d)
                cur.execute(sql)
                res = cur.fetchone()
                if cur.rowcount==0:
                    
                    sql='insert into bookings(user_id, bus_id, journey_date, seat) values({}, {}, "{}", 1)'.format(uid, u_b_id, d)
                    cur.execute(sql)
                    sql = 'insert into stats values({}, "{}", 19)'.format(u_b_id, d)
                    cur.execute(sql)
                    print("Ticket booked. Seat Number is 1. Go to my bookings for more details.")
                else:
                    if res[2]==0:
                        print("Sorry! The bus is full..")
                    else:
                        seat = 20-res[2]+1
                        sql='insert into bookings(user_id, bus_id, journey_date, seat) values({}, {}, "{}", {})'.format(uid, u_b_id,d, seat)
                        cur.execute(sql)
                        sql = 'update stats set availability=availability-1 where bus_id={} and journey_date="{}"'.format(u_b_id, d)
                        cur.execute(sql)
                        print("Ticket booked. Seat Number is ",seat,". Go to my bookings for more details.")
                cur.close()
        elif ch==2:
            cur = conn.cursor()
            sql= 'select booking_id, b1.bus_id, journey_date, seat, bus_from, bus_to, start_time, journey_time,arival_time, fare from bookings b1, buses b2 where b1.bus_id=b2.bus_id and user_id={}'.format(uid)
            cur.execute(sql)
            res = cur.fetchall()
            if len(res)==0:
                print("No data found...\n")
            else:
                print('{:<9}{:<5}{:<13}{:<6}{:<20}{:<20}{:<16}{:<16}{:<16}{:>5}'.format('Book_ID', 'BID', 'Date', 'Seat', 'From', 'To', 'Start Time', 'Duration', 'Arrival Time', 'Fare'))
                for row in res:
                    print('{:<9}{:<5}{:<13}{:<6}{:<20}{:<20}{:<16}{:<16}{:<16}{:>5}'.format(row[0],row[1],str(row[2]),row[3],row[4],row[5],str(row[6]),str(row[7]),str(row[8]),row[9]))
                    
            cur.close()
        elif ch==3:
            cur = conn.cursor()
            book_id = int(input("Enter booking id : "))
            sql = 'select bus_id, journey_date from bookings where booking_id = {}'.format(book_id)
            cur.execute(sql)
            b,dt = cur.fetchone()
            sql='update stats set availability=availability+1 where bus_id={} and journey_date="{}"'.format(b,dt)
            cur.execute(sql)
            sql = 'delete from bookings where booking_id={}'.format(book_id)
            cur.execute(sql)
            print("your booking has been cancelled and refund will be issued.")
            cur.close()
        elif ch==4:
            print("\nSigned Out...")
            break
        else:
            print("INVALID CHOICE")
            
    
def main():
    #Conneting to mysql
    h=input("Enter host name: ")
    u=input("Enter username: ")
    p=input("Enter password: ")
    if h=='':
        h='localhost'
    if u=='':
        u='root'
    if p=='':
        p='1234'
    conn=dbconnect(h,u,p)

    #init
    if conn==False:
        pass
    else:
        db = input("Enter database name : ")
        if db=='':
            db='bookings'
        init(db,conn)

        #Login
        menu = '''
        1. Sign in
        2. Register
        3. Exit
        '''
        uid=0
        print(menu)
        ch = int(input('Enter your choice : '))
        if ch==1:
            uid,uname = signin(conn)
        elif ch==2:
            if register(conn):
                uid,uname = signin(conn)
            else:
                pass
        elif ch==3:
            print("Exiting...")
            pass
        else:
            print("INVALID CHOICE")

        if uid==1:
            admin(conn)
        elif uid==0:
            pass
        else:
            user(uid,uname,conn) 

    #commit to the database
    conn.commit()
    conn.close()
    
main()




      


  

        
    


