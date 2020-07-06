from sqlalchemy import Table, Column, Integer, Float, String, Boolean, DateTime, Time, Date, MetaData, ForeignKey, create_engine, UniqueConstraint, CheckConstraint


link = 'postgres://postgres:1234@localhost/matrix'
engine = create_engine(link, echo = True) 

metadata = MetaData()

users = Table('users', metadata,
    Column('id', Integer, primary_key = True),
    Column('first_name', String(100), nullable = False),
    Column('last_name', String(100), nullable = False),
    Column('email', String(100), nullable = False,  unique = True),
    Column('password', String(100), nullable = False)
)

#esiste la tabella role solo per moderator e users, ma puo essere tranquillamente aggiornata per poter aggiungere altri ruoli
roles = Table('roles', metadata,
    Column('user_id', None, ForeignKey('users.id', ondelete='SET NULL'), nullable = True),
    Column('role', String(10), nullable = False)
)

cinema = Table('cinema', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable = False),
    Column('address', String(100), nullable = False)
)

halls = Table('halls', metadata,
    Column('id', Integer, primary_key = True),
    Column('hall_number', Integer, nullable = False),
    Column('rows', Integer, nullable = False),
    Column('columns', Integer, nullable = False),
    Column('cinema_id', None, ForeignKey('cinema.id'), nullable = False)
)

films = Table('films', metadata,
    Column('id', Integer, primary_key = True),
    Column('title', String(200), nullable = False),
    Column('duration', Integer, nullable = False),       #expressed in minutes
    Column('director', String(100), nullable = False),
    Column('year_prod', Date, nullable = False),
    Column('img_url', String(500)),
    Column('planned', Boolean, nullable=False),
    Column('category', String(100), nullable=False)
)

times = Table('times', metadata,
    Column('id', Integer, primary_key = True),
    Column('date', Date, nullable = False),
    Column('time', Time, nullable = False),
    Column('hall_id', None, ForeignKey('halls.id'), nullable = False),
    Column('film_id', None, ForeignKey('films.id'), nullable = False)
)

tickets = Table('tickets', metadata,
    Column('id', Integer, primary_key = True),
    Column('row', String(1), nullable = False),
    Column('seat', Integer, nullable = False),
    Column('price', Float, nullable = False),
    Column('cinema_id', None, ForeignKey('cinema.id'), nullable = False),
    Column('time_id', None, ForeignKey('times.id'), nullable = False),
    Column('user_id', None, ForeignKey('users.id', ondelete='SET NULL'), nullable = True),
    Column('film_id', None, ForeignKey('films.id'), nullable = False)
)

metadata.create_all(engine)
