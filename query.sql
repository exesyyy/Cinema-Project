-- query interessanti

-- query che restituisce Id, nome e cognome del cliente che ha speso di più
CREATE VIEW UsersTickets (UserId, UserFirstName, UserLastName, TicketsNumber, Price) AS 
SELECT users.id, users.first_name, users.last_name, COUNT(*), SUM(tickets.price) 
FROM users JOIN tickets ON users.id = tickets.user_id 
GROUP BY users.id;

SELECT UserId, UserFirstName, UserLastName, Price
FROM UsersTickets 
WHERE Price = (SELECT MAX(Price) 
                FROM UsersTickets);



-- query che restituisce il titolo del film più visto (ovvero quello con più biglietti acquistati)
CREATE VIEW FilmTickets (IdFilm, FilmTitle, Tickets) AS 
SELECT films.id, films.title, COUNT(*) 
FROM films JOIN tickets ON films.id =tickets.film_id 
GROUP BY films.id;

SELECT FilmTitle 
FROM FilmTickets 
WHERE Tickets = (SELECT MAX(Tickets) 
                 FROM FilmTickets);



-- query utile al moderatore per capire gli orari in cui una determinata sala è occupata
-- in un giorno specificato
SELECT times.time 
FROM halls JOIN times ON halls.id = times.hall_id 
WHERE halls.hall_number = 2 AND times.date = '10-05-2020';




-- query per statistiche moderatori (incasso totale per ogni film)
SELECT films.id, films.title, SUM(tickets.price) AS Incasso_totale
FROM films JOIN tickets ON films.id = tickets.film_id 
GROUP BY films.id, films.title 
ORDER BY films.title;



-- query per vedere il numero di persone che hanno visualizzato un film
SELECT films.title, COUNT(tickets.id) AS Visualizzazioni 
FROM films LEFT JOIN tickets ON films.id = tickets.film_id 
GROUP BY films.id, films.title 
ORDER BY films.title;



-- posti a sedere per ogni sala
SELECT halls.hall_number, halls.rows * halls.columns AS posti_a_sedere 
FROM halls 
GROUP BY halls.id, halls.hall_number;





-- query che restituisce il numero di posti totali rispetto ai film
CREATE VIEW movieseats (times_id, film_id, posti) AS
SELECT times.id, times.film_id, halls.rows * halls.columns AS posti_a_sedere
FROM times JOIN halls ON times.hall_id = halls.id
ORDER BY times.film_id;

SELECT film_id, films.title, SUM(movieseats.posti) AS posti_totali
FROM movieseats JOIN films ON movieseats.film_id = films.id
GROUP BY film_id, films.title
ORDER BY film_id; 
