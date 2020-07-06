from tabinit import users, halls, times, tickets, cinema, roles, films
from sqlalchemy import create_engine

link = 'postgres://postgres:1234@localhost/matrix'
engine = create_engine(link, echo = True) 

conn = engine.connect()


ins = users.insert()

conn.execute(ins, [
     {'first_name': 'Tommaso', 'last_name': 'Golfetto', 'email': 'tommaso.golfetto@gmail.com', 'password': '123456'},
     {'first_name': 'Marco', 'last_name': 'Serena', 'email': 'marcoserena96@gmail.com', 'password': '123456'},
     {'first_name': 'Aldo', 'last_name': 'Baglio', 'email': 'aldobaglio@gmail.com', 'password': '123456'}
])


ins = cinema.insert()
conn.execute(ins, [
     {'name': 'from unive import degree', 'address': 'Sq. Screenwriter 101, Hollywood'}
])


ins = roles.insert()
conn.execute(ins, [
     {'user_id': 1, 'role': 'moderator'},
     {'user_id': 2, 'role': 'student'}
])





ins = halls.insert()
conn.execute(ins, [
     {'hall_number': '1', 'rows': '14', 'columns': '15', 'cinema_id': 1},
     {'hall_number': '2', 'rows': '12', 'columns': '10', 'cinema_id': 1},
     {'hall_number': '3', 'rows': '10', 'columns': '14', 'cinema_id': 1},
     {'hall_number': '4', 'rows': '20', 'columns': '24', 'cinema_id': 1},
     {'hall_number': '5', 'rows': '17', 'columns': '19', 'cinema_id': 1},
     {'hall_number': '6', 'rows': '13', 'columns': '17', 'cinema_id': 1},
     {'hall_number': '7', 'rows': '15', 'columns': '19', 'cinema_id': 1}

])


ins = films.insert()
conn.execute(ins, [
     {'title': 'Oblivion', 'duration': '124', 'director' : 'Joseph Kosinski', 'year_prod': '15-08-2013', 'img_url': 'https://aforismi.meglio.it/img/film/Oblivion-poster.jpg', 'planned': True, 'category':'adventure', 'cinema_id': 1},
     {'title': 'Star Wars - Return of the jedi', 'duration': '136', 'director' : 'Richard Marquand', 'year_prod': '20-02-2012', 'img_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/1200px-Star_Wars_Logo.svg.png','planned': True, 'category':'fantasy', 'cinema_id': 1},
     {'title': 'Avengers - Endgame', 'duration': '182', 'director' : 'Joe Russo & Anthony Russo', 'year_prod': '30-07-2016', 'img_url': 'https://pad.mymovies.it/filmclub/2018/12/029/locandina.jpg', 'planned': True, 'category':'fantasy', 'cinema_id': 1},
     {'title': 'The Amazing Spiderman', 'duration': '153', 'director' : 'Marc Webb', 'year_prod': '01-12-2018', 'img_url': 'https://images-na.ssl-images-amazon.com/images/I/A1FNoFlnDnL._AC_SL1500_.jpg', 'planned': True, 'category':'action', 'cinema_id': 1},
     {'title': 'Hot Fuzz', 'duration': '121', 'director' : 'Edgar Wright', 'year_prod': '22-08-2019', 'img_url': 'https://pad.mymovies.it/filmclub/2007/02/171/locandina.jpg', 'planned': True, 'category':'comedy', 'cinema_id': 1},
     {'title': 'Tre uomini e una gamba', 'duration': '160', 'director' : 'Massimo Venier', 'year_prod': '27-12-1997', 'img_url': 'https://images-na.ssl-images-amazon.com/images/I/71Iq4IF29iL._SL1024_.jpg', 'planned': True, 'category':'comedy', 'cinema_id': 1},
     {'title': 'Fast & Furious 8', 'duration': '149', 'director' : 'F. Gary Gary', 'year_prod': '13-05-2017', 'img_url': 'https://images-na.ssl-images-amazon.com/images/I/91jzAhhTxVL._SL1500_.jpg', 'planned': True, 'category':'action', 'cinema_id': 1},
     {'title': 'The Transporter', 'duration': '164', 'director' : 'Olivier Megaton', 'year_prod': '09-05-2015', 'img_url': 'https://aforismi.meglio.it/img/film/The_transporter.jpg', 'planned': True, 'category':'action', 'cinema_id': 1},
     {'title': 'Chiedimi se sono felice', 'duration': '160', 'director' : 'Massimo Venier', 'year_prod': '15-12-2000', 'img_url': 'https://images-na.ssl-images-amazon.com/images/I/61FyDOxJLPL._SY445_.jpg', 'planned': True, 'category':'comedy', 'cinema_id': 1},
     {'title': 'Avatar', 'duration': '162', 'director' : 'James Cameron', 'year_prod': '15-01-2010', 'img_url': 'https://pad.mymovies.it/filmclub/2008/03/090/locandina.jpg', 'planned': True, 'category':'fantasy', 'cinema_id': 1},
     {'title': 'Black Widow', 'duration': '130', 'director' : 'Cate Shortland', 'year_prod': '24-04-2020', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSN0K42yCGmjwvfznnDQyr_wLR71WmCo2DGvQ&usqp=CAU', 'planned': True, 'category':'adventure', 'cinema_id': 1},
     {'title': 'Rogue Il Solitario', 'duration': '103', 'director' : 'Phillip Atwell', 'year_prod': '24-08-2007', 'img_url': 'https://pad.mymovies.it/filmclub/2007/05/089/locandina.jpg', 'planned': True, 'category':'action', 'cinema_id': 1},
     {'title': 'Borat', 'duration': '86', 'director' : 'Larry Charles',  'year_prod': '12-01-2010', 'img_url': 'https://vivoinlomellina.files.wordpress.com/2015/10/borat2.jpg','planned': False, 'category':'comedy', 'cinema_id': 1},
])



ins = times.insert()
conn.execute(ins, [
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 4, 'film_id': 1},      
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 5, 'film_id': 1},      
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 6, 'film_id': 2},      
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 7, 'film_id': 4},      
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 1, 'film_id': 5},      
     {'date': '29-06-2020', 'time':'19:30', 'hall_id': 2, 'film_id': 6},      
     {'date': '29-06-2020', 'time':'21:30', 'hall_id': 3, 'film_id': 6},      
     {'date': '29-06-2020', 'time':'23:30', 'hall_id': 1, 'film_id': 6},      
     {'date': '29-06-2020', 'time':'21:30', 'hall_id': 2, 'film_id': 9},      
     {'date': '29-06-2020', 'time':'19:00', 'hall_id': 3, 'film_id': 7},      
     {'date': '29-06-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 8},      
     {'date': '29-06-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 8},      
     {'date': '29-06-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 8},      
     {'date': '29-06-2020', 'time':'21:00', 'hall_id': 7, 'film_id': 9},      
     {'date': '29-06-2020', 'time':'18:00', 'hall_id': 1, 'film_id': 10},     
     {'date': '29-06-2020', 'time':'20:00', 'hall_id': 2, 'film_id': 10},     
     {'date': '29-06-2020', 'time':'23:00', 'hall_id': 3, 'film_id': 11},     
     {'date': '29-06-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 12},     
     {'date': '29-06-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 12},     
     {'date': '29-06-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 12},
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 4, 'film_id': 1},      
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 5, 'film_id': 2},      
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 6, 'film_id': 3},      
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 7, 'film_id': 4},      
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 1, 'film_id': 5},      
     {'date': '30-06-2020', 'time':'19:30', 'hall_id': 2, 'film_id': 6},      
     {'date': '30-06-2020', 'time':'21:30', 'hall_id': 3, 'film_id': 6},      
     {'date': '30-06-2020', 'time':'23:30', 'hall_id': 1, 'film_id': 6},      
     {'date': '30-06-2020', 'time':'21:30', 'hall_id': 2, 'film_id': 7},      
     {'date': '30-06-2020', 'time':'19:00', 'hall_id': 3, 'film_id': 7},      
     {'date': '30-06-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 8},      
     {'date': '30-06-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 8},      
     {'date': '30-06-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 8},      
     {'date': '30-06-2020', 'time':'21:00', 'hall_id': 7, 'film_id': 9},      
     {'date': '30-06-2020', 'time':'18:00', 'hall_id': 1, 'film_id': 10},     
     {'date': '30-06-2020', 'time':'20:00', 'hall_id': 2, 'film_id': 10},     
     {'date': '30-06-2020', 'time':'23:00', 'hall_id': 3, 'film_id': 11},     
     {'date': '30-06-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 12},     
     {'date': '30-06-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 12},     
     {'date': '30-06-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 12},
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 4, 'film_id': 1},      
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 5, 'film_id': 2},      
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 6, 'film_id': 3},      
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 7, 'film_id': 4},      
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 1, 'film_id': 5},      
     {'date': '01-07-2020', 'time':'19:30', 'hall_id': 2, 'film_id': 6},      
     {'date': '01-07-2020', 'time':'21:30', 'hall_id': 3, 'film_id': 6},      
     {'date': '01-07-2020', 'time':'23:30', 'hall_id': 1, 'film_id': 6},      
     {'date': '01-07-2020', 'time':'21:30', 'hall_id': 2, 'film_id': 7},      
     {'date': '01-07-2020', 'time':'19:00', 'hall_id': 3, 'film_id': 7},      
     {'date': '01-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 8},      
     {'date': '01-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 8},      
     {'date': '01-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 8},      
     {'date': '01-07-2020', 'time':'21:00', 'hall_id': 7, 'film_id': 9},      
     {'date': '01-07-2020', 'time':'18:00', 'hall_id': 1, 'film_id': 10},     
     {'date': '01-07-2020', 'time':'20:00', 'hall_id': 2, 'film_id': 10},     
     {'date': '01-07-2020', 'time':'23:00', 'hall_id': 3, 'film_id': 11},     
     {'date': '01-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 12},     
     {'date': '01-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 12},     
     {'date': '01-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 12},
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 4, 'film_id': 1},      
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 5, 'film_id': 2},      
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 6, 'film_id': 3},      
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 7, 'film_id': 4},      
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 1, 'film_id': 5},      
     {'date': '02-07-2020', 'time':'19:30', 'hall_id': 2, 'film_id': 6},      
     {'date': '02-07-2020', 'time':'21:30', 'hall_id': 3, 'film_id': 6},      
     {'date': '02-07-2020', 'time':'23:30', 'hall_id': 1, 'film_id': 6},      
     {'date': '02-07-2020', 'time':'21:30', 'hall_id': 2, 'film_id': 7},      
     {'date': '02-07-2020', 'time':'19:00', 'hall_id': 3, 'film_id': 7},      
     {'date': '02-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 8},      
     {'date': '02-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 8},      
     {'date': '02-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 8},      
     {'date': '02-07-2020', 'time':'21:00', 'hall_id': 7, 'film_id': 9},      
     {'date': '02-07-2020', 'time':'18:00', 'hall_id': 1, 'film_id': 10},     
     {'date': '02-07-2020', 'time':'20:00', 'hall_id': 2, 'film_id': 10},     
     {'date': '02-07-2020', 'time':'23:00', 'hall_id': 3, 'film_id': 11},     
     {'date': '02-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 12},     
     {'date': '02-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 12},     
     {'date': '02-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 12},
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 4, 'film_id': 1},      
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 5, 'film_id': 2},      
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 6, 'film_id': 3},      
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 7, 'film_id': 4},      
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 1, 'film_id': 5},      
     {'date': '03-07-2020', 'time':'19:30', 'hall_id': 2, 'film_id': 6},      
     {'date': '03-07-2020', 'time':'21:30', 'hall_id': 3, 'film_id': 6},      
     {'date': '03-07-2020', 'time':'23:30', 'hall_id': 1, 'film_id': 6},      
     {'date': '03-07-2020', 'time':'21:30', 'hall_id': 2, 'film_id': 7},      
     {'date': '03-07-2020', 'time':'19:00', 'hall_id': 3, 'film_id': 7},      
     {'date': '03-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 8},      
     {'date': '03-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 8},      
     {'date': '03-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 8},      
     {'date': '03-07-2020', 'time':'21:00', 'hall_id': 7, 'film_id': 9},      
     {'date': '03-07-2020', 'time':'18:00', 'hall_id': 1, 'film_id': 10},     
     {'date': '03-07-2020', 'time':'20:00', 'hall_id': 2, 'film_id': 10},     
     {'date': '03-07-2020', 'time':'23:00', 'hall_id': 3, 'film_id': 11},     
     {'date': '03-07-2020', 'time':'19:00', 'hall_id': 4, 'film_id': 12},     
     {'date': '03-07-2020', 'time':'21:00', 'hall_id': 5, 'film_id': 12},     
     {'date': '03-07-2020', 'time':'23:00', 'hall_id': 6, 'film_id': 12}                
])


ins = tickets.insert()
conn.execute(ins, [
     {'row': 'A', 'seat': '3', 'price': '0.00', 'cinema_id': 1, 'time_id': 2, 'user_id': 1, 'film_id': 1},
     {'row': 'L', 'seat': '4', 'price': '0.00', 'cinema_id': 1, 'time_id': 3, 'user_id': 1, 'film_id': 2},
     {'row': 'F', 'seat': '5', 'price': '5.50', 'cinema_id': 1, 'time_id': 3, 'user_id': 2, 'film_id': 2},
     {'row': 'F', 'seat': '6', 'price': '5.50', 'cinema_id': 1, 'time_id': 3, 'user_id': 2, 'film_id': 2},
     {'row': 'F', 'seat': '7', 'price': '5.50', 'cinema_id': 1, 'time_id': 3, 'user_id': 2, 'film_id': 2},
     {'row': 'A', 'seat': '1', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},  
     {'row': 'A', 'seat': '2', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'A', 'seat': '3', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'A', 'seat': '4', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'A', 'seat': '5', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'A', 'seat': '6', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'A', 'seat': '7', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '1', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '2', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '3', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '4', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '5', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '6', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'C', 'seat': '7', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'D', 'seat': '6', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'E', 'seat': '1', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'E', 'seat': '2', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
     {'row': 'E', 'seat': '3', 'price': '10.00', 'cinema_id': 1, 'time_id': 9, 'user_id': 3, 'film_id': 9},
])