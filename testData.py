from models.admin import Show,Tag,Venue,tags,Language,Allocation, BookTicket
from models.users import User
from werkzeug.security import generate_password_hash
from datetime import date, time, datetime
from flask_login import current_user

def generateTestData(app,db):
    with app.app_context():
        db.drop_all()
        db.create_all()

        action = Tag(name='Action')
        thriller = Tag(name='Thriller')
        drama = Tag(name='Drama')
        fantasy = Tag(name='Fantasy')
        horror = Tag(name='Horror')
        mystery = Tag(name='Mystery')
        comedy = Tag(name='Comedy')


        hindi = Language(name='Hindi')
        english = Language(name='English')
        bengali = Language(name='Bengali')
        tamil = Language(name='Tamil')
        telugu = Language(name='Telegu')
        malayalam = Language(name='Malayalam')

        
        venue1 = Venue(name='Inox Forum Mall',location='Kasba',city='Kolkata',capacity=340,description='One of the biggest malls in Kolkata',timestamp=datetime(2023,3,1,11,21,00))
        db.session.add(venue1)
        venue2 = Venue(name='Inox Acropolis Mall',location='Rabindra Sadan',city='Kolkata',capacity=210,description='One of the most popular malls in Kolkata',timestamp=datetime(2023,2,18,9,21,00))
        db.session.add(venue2)
        venue3 = Venue(name='Inox Rangoli Mall',location='Liluah',city='Howrah',capacity=400,description='One of the most unique malls in Kolkata',timestamp=datetime(2023,1,13,18,21,00))
        db.session.add(venue3)

        for i in range(8):
            venueNew = Venue(name='Mall Number '+str(i),location='Loc'+str(i),city='Howrah',capacity=400,description='One of the most unique malls in Kolkata',timestamp=datetime(2022,i+1,i+10,11,i+2,00))
            db.session.add(venueNew)

        db.session.add(action)
        db.session.add(thriller)
        db.session.add(horror)
        db.session.add(mystery)
        db.session.add(fantasy)
        db.session.add(drama)
        db.session.add(comedy)

        db.session.add(hindi)
        db.session.add(english)
        db.session.add(bengali)
        db.session.add(tamil)
        db.session.add(telugu)
        db.session.add(malayalam)

        show1 = Show(name='Quantamania',rating=10,duration='2 hr 30 min',timestamp=datetime.now())
        show1.tags.append(action)
        show1.tags.append(drama)
        show1.languages.append(hindi)
        show1.languages.append(malayalam)
        db.session.add(show1)

        show2 = Show(name='AntMan and the Wasp',rating=7,duration='3 hrs 2 min',timestamp=datetime.now())
        show2.tags.append(thriller)
        show2.tags.append(horror)
        show2.languages.append(bengali)
        show2.languages.append(telugu)
        db.session.add(show2)
        
        show3 = Show(name='গোলোকধাধা',rating=5,duration='4 hrs',timestamp=datetime.now())
        show3.tags.append(fantasy)
        show3.tags.append(mystery)
        show3.languages.append(bengali)
        show3.languages.append(hindi)
        db.session.add(show3)

        for i in range(100):
            show4 = Show(name='Anthem'+str(i),rating=2,duration='2 hrs 50 min',timestamp=datetime.now())
            show4.tags.append(drama)
            show4.tags.append(fantasy)
            show4.languages.append(tamil)
            show4.languages.append(telugu)
            db.session.add(show4)


        allocDetails1 = Allocation(venue_id=1,show_id=1,timeslot=datetime(2023, 12, 25, 11, 00, 00),totSeats=120,avSeats=100,price=234.50)
        allocDetails2 = Allocation(venue_id=1,show_id=2,timeslot=datetime(2021, 2, 15, 9, 5, 00),totSeats=150,avSeats=80,price=430.50)
        allocDetails3 = Allocation(venue_id=2,show_id=3,timeslot=datetime(2020, 2, 8, 7, 5, 00),totSeats=210,avSeats=20,price=330.50)
        allocDetails4 = Allocation(venue_id=2,show_id=2,timeslot=datetime(2020, 2, 8, 8, 5, 00),totSeats=210,avSeats=20,price=330.50)
        allocDetails5 = Allocation(venue_id=2,show_id=4,timeslot=datetime(2020, 2, 8, 9, 5, 00),totSeats=210,avSeats=20,price=330.50)
        
        allocDetails6 = Allocation(venue_id=2,show_id=1,timeslot=datetime(2023, 3, 22, 10, 5, 00),totSeats=210,avSeats=20,price=330.50)
        allocDetails8 = Allocation(venue_id=2,show_id=1,timeslot=datetime(2023, 3, 23, 11, 5, 00),totSeats=210,avSeats=20,price=330.50)
        allocDetails9 = Allocation(venue_id=2,show_id=1,timeslot=datetime(2023, 3, 25, 12, 5, 00),totSeats=210,avSeats=20,price=330.50)
        allocDetails10 = Allocation(venue_id=2,show_id=1,timeslot=datetime(2023, 3, 27, 9, 5, 00),totSeats=210,avSeats=0,price=330.50)
        allocDetails11 = Allocation(venue_id=2,show_id=1,timeslot=datetime(2023, 3, 26, 9, 5, 00),totSeats=210,avSeats=20,price=330.50)
        
        allocDetails7 = Allocation(venue_id=2,show_id=6, timeslot=datetime(2020, 2, 8, 11, 5, 00),totSeats=210,avSeats=20,price=330.50)
        db.session.add(allocDetails1)
        db.session.add(allocDetails2)
        db.session.add(allocDetails3)
        db.session.add(allocDetails4)
        db.session.add(allocDetails5)
        db.session.add(allocDetails6)
        db.session.add(allocDetails7)
        db.session.add(allocDetails8)
        db.session.add(allocDetails9)
        db.session.add(allocDetails10)
        db.session.add(allocDetails11)

        bookT1 = BookTicket(user_email='test@gmail.com',allocSeats=3,totPrice=345.50,timestamp=datetime.now())
        bookT1.allocShow = allocDetails1
        db.session.add(bookT1)
        bookT1 = BookTicket(user_email='test@gmail.com',allocSeats=7,totPrice=1200.50,timestamp=datetime.now())
        bookT1.allocShow = allocDetails1
        db.session.add(bookT1)


        db.session.add(User(name='Admin User',email='admin@gmail.com',password=generate_password_hash('admin123', method='sha256'),access=1))
        db.session.add(User(name='Test User',email='test@gmail.com',password=generate_password_hash('1234', method='sha256'),access=0))
        db.session.commit()

    #@app.before_first_request
    #def create_admin():
       #db.session.commit()