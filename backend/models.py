from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String(50), nullable=False)
    Lastname = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password_Hash = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(20), nullable=False, default='customer')

class Customer(db.Model):
    __tablename__ = 'customer'
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String(50), nullable=False)
    Lastname = db.Column(db.String(50), nullable=False)
    Contact_Number = db.Column(db.String(15), nullable=False)

class Barber(db.Model):
    __tablename__ = 'barber'
    Barber_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Barber_Name = db.Column(db.String(100), nullable=False)
    Contact_Number = db.Column(db.String(15), nullable=False)

class BarberSchedule(db.Model):
    __tablename__ = 'barber_schedule'
    Schedule_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Barber_ID = db.Column(db.Integer, db.ForeignKey('barber.Barber_ID'), nullable=False)
    Day = db.Column(db.String(10), nullable=False)
    Start_Time = db.Column(db.Time, nullable=False)
    End_Time = db.Column(db.Time, nullable=False)

class Services(db.Model):
    __tablename__ = 'services'
    Services_Code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Service_Name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Numeric(8, 2), nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservation'
    Reservation_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('customer.Customer_ID'), nullable=False)
    Barber_ID = db.Column(db.Integer, db.ForeignKey('barber.Barber_ID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    Time = db.Column(db.Time, nullable=False)
    Status = db.Column(db.String(20), nullable=False, default='Pending')
    DP_Amount = db.Column(db.Numeric(8, 2), nullable=False)
    DP_Status = db.Column(db.String(10), nullable=True)

class ServicesAvailed(db.Model):
    __tablename__ = 'services_availed'
    Reservation_ID = db.Column(db.Integer, db.ForeignKey('reservation.Reservation_ID'), primary_key=True, nullable=False)
    Services_Code = db.Column(db.Integer, db.ForeignKey('services.Services_Code'), primary_key=True, nullable=False)
    Service_Price = db.Column(db.Numeric(8, 2), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    Discount = db.Column(db.Numeric(8, 2), nullable=True, default=0.00)