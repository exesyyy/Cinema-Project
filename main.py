from flask import Flask, render_template, json, redirect, url_for, session, flash, request
from sqlalchemy import create_engine, select, func, Table, MetaData
from flask_login import login_user, logout_user, login_required
from datetime import timedelta, date, datetime
from tabinit import users, roles, cinema, halls, films, times, tickets
import logging

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=60)


link = 'postgres://postgres:1234@localhost/matrix'
engine = create_engine(link, echo = False) 

conn = engine.connect()



@app.route('/home')
@app.route('/')
def home():    
    if "user" in session:
        return render_template("home.html", user=session["user"])    
    return render_template('home.html')



@app.route('/registration')
def registration():
    return render_template('registration.html')



@app.route('/success', methods = ['GET', 'POST'])
def success():
    user_email = request.form['email']

    q = select([users]).\
        where(users.c.email == user_email)
    check = conn.execute(q).scalar()
    #controllo se l'utente che sta provando a registrarsi è già registrato con la mail inserita
    if check:
        flash(f"Registrazione fallita, email già presente!!!")
    else:
        user_name = request.form['user_name']
        user_surname = request.form['user_lastname']    
        user_pass = request.form['password']
        ins = users.insert()
        conn.execute(ins, [
            {'first_name': user_name, 'last_name': user_surname, 'email':user_email, 'password':user_pass}
        ])
        flash(f"Registrazione avvenuta con successo!")
    return redirect(url_for('home'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #seleziono l'email
        user_email = request.form['email']
        q = select([users]).\
            where(users.c.email == user_email)
        check = conn.execute(q).scalar()
        #controllo se l'email è presente nel database
        if check:
            #se è presente procedo al controllo della password
            q = select([users.c.password]).where(users.c.email == user_email)
            res = conn.execute(q).fetchone()['password']
            #confronto la password digitata con quella presente nel database
            if(request.form['password'] == res):
                #in caso positivo prendo il nome utente per usaro nella navbar
                q = select([users]).where(users.c.email == user_email)
                session["user"] = conn.execute(q).fetchone()['first_name']
                session["user_id"] = conn.execute(q).fetchone()['id']
                session.permanent = True
                #Controllo se l'utente ha un ruolo e salvo la risposta nella sessione
                q = select([roles.c.role]).where(roles.c.user_id == session["user_id"])
                role = conn.execute(q).fetchone()
                if role:
                    if role[0] == "moderator":
                        session['role'] = 'moderator'                    
                    else:
                        session['role'] = 'student'
                else:
                    session['role'] = None
                return redirect(url_for('home'))
            else:
                #password sbagliata
                flash(f"Incorrect Password!", "info")
                return redirect(url_for('login'))
        else:
            #email sbagliata            
            flash(f"Incorrect Email!", "info")
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/logout')
def logout():
    if "user" in session:
        flash(f"Successfully logged out", "info")
    #rimuovo dalla sessione tutti i dati relativi all'utente e alle eventuali ricerche che ha fatto sui film
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("role", None)
    session.pop("filmdate", None)
    session.pop("category", None)

    return render_template("home.html")



@app.route('/user')
def user():
    #Controllo se l'utente è un moderatore    
    if session['role'] == 'moderator':
        #Calcolo dei dati statistici per ogni film
        q = select([users.c.id, users.c.email])
        ut = conn.execute(q).fetchall()
        utenti = []
        for u in ut:
            r = dict(id=u[0], email=u[1])
            utenti.append(r)
        q = select([roles.c.user_id, users.c.email, roles.c.role]).select_from(
            roles.join(users, roles.c.user_id == users.c.id))
        user_roles = conn.execute(q).fetchall()
        lista = []
        #Ricaviamo il numero di visualizzazioni totali per ogni film
        q = select([films.c.id, films.c.title, func.count(tickets.c.id)]).select_from(
            films.join(tickets, films.c.id == tickets.c.film_id, isouter=True)).\
            group_by(films.c.id, films.c.title).\
            order_by(films.c.id)
        vis = conn.execute(q).fetchall()
        for v in vis:
            d = dict(id=v[0], title=v[1], visual=v[2])
            lista.append(d)

        #Ricaviamo l'incasso totale per ogni film
        q = select([films.c.id, func.sum(tickets.c.price)]).select_from(
            films.join(tickets, films.c.id == tickets.c.film_id, isouter=True)).\
            group_by(films.c.id).\
            order_by(films.c.id)
        pri = conn.execute(q).fetchall()
        for p in pri:
            pr = p[1]
            if p[1] == None:
                pr = 0.0    
            lista[p[0]-1].update(dict(price=pr))
        return render_template("moderator.html", user=session["user"], users=utenti, roles=user_roles, lista=lista)
    else:
        #Se l'utente non è un moderatore nella sua area riservata troverà la lista di film visti
        q = select([films.c.title, films.c.img_url]).select_from(
            tickets.join(users, tickets.c.user_id == session['user_id']).join(films, films.c.id == tickets.c.film_id)
        ).distinct()
        res = conn.execute(q).fetchall()
        return render_template("user.html", lista=res, user=session["user"])



@app.route('/films', methods=['GET','POST'])
def film():
    today = date.today()
    now = datetime.now().strftime("%H:%M:%S")
    if request.method == 'GET':
        session['category'] = ''        
        session['filmdate'] = today
    else:
        session['category'] = request.form['cat']
        session['filmdate'] = request.form['filmdate']

    #Seleziono tutti i film senza distinzione di categoria
    if  session['category'] == '' :
        #Seleziono la lista di film in programmazione
        q = select([films.c.id, films.c.title, films.c.duration, films.c.director, films.c.img_url, films.c.year_prod, films.c.category]).where(films.c.planned == True)
        film_list = conn.execute(q).fetchall()
        #Seleziono gli orari per ogni film in programmazione nella giornata odierna che hanno orario seguente al momento della richiesta
        q = select([films.c.id, times.c.time, times.c.id]).select_from(
            times.join(films, films.c.id == times.c.film_id)
        ).where((films.c.planned==True) & (times.c.date==session['filmdate']) & (times.c.time>now))
        times_list = conn.execute(q).fetchall()
    #Condizione in cui voglio mostrare solo i film di una categoria selezionata
    else:
        q = select([films.c.id, films.c.title, films.c.duration, films.c.director, films.c.img_url, films.c.year_prod, films.c.category]).where((films.c.planned == True) & (films.c.category == session['category']))
        film_list = conn.execute(q).fetchall()
        #Seleziono gli orari per ogni film in programmazione nella giornata odierna che hanno orario seguente al momento della richiesta
        q = select([films.c.id, times.c.time, times.c.id]).select_from(
            times.join(films, films.c.id == times.c.film_id)
        ).where((films.c.planned==True) & (times.c.date==session['filmdate']) & (films.c.category == session['category']) & (times.c.time>now))
        times_list = conn.execute(q).fetchall()
        if not film_list:
            flash(f"Non ci sono film nella categoria '{session['category']}' o la categoria non esiste")

    final = []
    for f in film_list:
        r = dict(id=f[0], title=f[1], duration=f[2], director=f[3], url=f[4], year=f[5], cat=f[6])
        l=[]
        for h in times_list:
            if f[0] == h[0]:
                l.append(dict(orario=h[1],id_orario=h[2]))
        r.update(dict(orari=l))
        final.append(r)    

    #Seleziono i film non in programmazione in modo da passarli come parametro quando un utente è moderatore
    if "user" in session:
        if session['role'] == 'moderator':
            #NUM_SALE CI SERVE PER LA PARTE DI INSERIMENTO DI UN ORARIO (SELEZIONO LA SALA DI RIPRODUZIONE NEL DROPDOWN)
            q = select([func.count()]).select_from(halls)
            num_sale = conn.execute(q).scalar()
            q = select([films.c.id, films.c.title]).where(films.c.planned == False)
            notplanned = conn.execute(q).fetchall()          
            return render_template("films.html", lista=final, user=session['user'], moderator=True, sale=num_sale, notplanned=notplanned, date=session['filmdate'], cat=session['category'], today=today)

        return render_template("films.html", lista=final, user=session['user'], date=session['filmdate'], cat=session['category'], today=today)
    return render_template("films.html", lista=final, date=session['filmdate'], cat=session['category'], today=today)



@app.route('/hall', methods=['GET','POST'])
def hall():
    #se l'utente non ha fatto l'accesso, non potrà accedere alla prenotazione dei biglietti
    if "user" in session:        
        id_orario = request.form.get('occupied')
        session['orario'] = id_orario
        q = select([halls.c.rows, halls.c.columns]).select_from(halls.\
                join(times, times.c.hall_id == halls.c.id)).\
                where(times.c.id==id_orario)
        hall = conn.execute(q).fetchall()
        rows = hall[0][0]
        columns = hall[0][1]

        #seleziono i biglietti relativi all'orario che ho premuto
        #mi serviranno per costruire la sala con i relativi posti occupati
        q  = select([tickets]).select_from(tickets.\
                join(times, tickets.c.time_id == id_orario))
        biglietti = conn.execute(q).fetchall()
        #id, row, seat, price, cinema_id, time_id, user_id, film_id
        sala = [[0 for x in range(rows)] for y in range(columns)]

        for b in biglietti:
            if b[6] == session['user_id']:
                sala[ord(b[1])-ord('A')][b[2]-1] = 1
            else:
                sala[ord(b[1])-ord('A')][b[2]-1] = -1
        
        return render_template("hall.html", sala=sala, user=session['user'], idOrario=id_orario)
    else:
        flash(f"You must be logged for access the ticket page!", "info")
        return redirect(url_for('login'))




#++++++++++++++++++++++++++++++++++++++++++++++++++
#   SEZIONE RELATIVA ALL'AGGIORNAMENTO DEI FILM
#++++++++++++++++++++++++++++++++++++++++++++++++++

#Inserimento di un nuovo film all'interno del database
@app.route('/filminsert', methods = ['POST'])
def filminsert():
    film_title = request.form['title']
    q = select([films]).\
        where(films.c.title == film_title)
    check = conn.execute(q).scalar()
    #controllo se il film è già presente nel database
    if check:
        #se è presente invio un messaggio d'errore che avverte della presenza
        flash(f"Film already present in the list!")
    else:
        #procedo all'inserimento del nuovo film nel database
        film_url = request.form['imgurl']
        film_date = request.form['filmdate']
        film_category = request.form['category']
        film_dur = request.form['duration']
        film_dir = request.form['director']

        ins = films.insert()
        conn.execute(ins,[
            {'title': film_title, 'duration':film_dur, 'director':film_dir, 'year_prod': film_date, 'img_url': film_url ,'planned': True, 'category': film_category}
        ])
        flash(f"Film successfully added!")
    return redirect(url_for('film'))


#Inserimento degli orari relativi ad un film
@app.route('/timeinsert', methods=['GET', 'POST'])
def timeinsert():
    if request.method == 'POST':
        todo = request.form.to_dict()
        film = todo.get("filmSelected")
        x = 1
        var_ora = "mytime" + str(x)
        var_sala = "selectedhall" + str(x)
        var_data = "mydate" + str(x)
        while todo.get(var_ora):
            orario = todo.get(var_ora)
            sala = todo.get(var_sala)
            data = todo.get(var_data)
            x += 1
            #return f"{film} - {data} - {orario} - {sala}"
            ins = times.insert()
            conn.execute(ins,[
                {'date': data, 'time': orario, 'hall_id': sala, 'film_id': film}
            ])
            var_ora = "mytime" + str(x)
            var_sala = "selectedhall" + str(x)
            var_data = "mydate" + str(x)
    flash(f"Orari inseriti correttamente")
    return redirect(url_for('film'))


#Rimozione di un orario specificato (Non devono essere stati acquistati biglietti in quell'orario)
@app.route('/timeremove', methods=['GET', 'POST'])
def timeremove():
    if request.method == 'POST':
        film_id = request.form.get('timeremoved')
        old_time = request.form['removetime']
        old_date = request.form['removedate']
        q = select([times]).\
            where((times.c.time == old_time ) & (times.c.date == old_date) & (times.c.film_id == film_id))
        check = conn.execute(q).scalar()
        if check:
            d = times.delete().where((times.c.time == old_time ) & (times.c.date == old_date) & (times.c.film_id == film_id))
            conn.execute(d)
            flash(f"Orario rimosso con successo!")
        else:
            flash(f"L'orario non è presente nella data specificata!")
    return redirect(url_for('film'))

    
#Modifica dei dati di un film, possono essere cambiati in modo indipendente uno dall'altro
@app.route('/filmmodify', methods=['GET','POST'])
def filmmodify():
    film_id = request.form.get('filmModified')
    new_title = request.form['modifytitle']
    new_url = request.form['modifyurl']
    new_date = request.form['modifydate']
    new_cat = request.form['modifycat']
    
    if film_id != 'Seleziona un film':
        if new_title:
            u = films.update().where(films.c.id == film_id).values(title = new_title)
            conn.execute(u)
        if new_url:
            u = films.update().where(films.c.id == film_id).values(img_url = new_url)
            conn.execute(u)
        if new_date:
            u = films.update().where(films.c.id == film_id).values(date = new_date)
            conn.execute(u)
        if new_cat:
            u = films.update().where(films.c.id == film_id).values(category = new_cat)
            conn.execute(u)
        flash(f"Film successfully updated!")
    else:
        flash(f"Non è stato selezionato alcun film")    
    return redirect(url_for('film'))



#Ripianificazione di un film nella lista di quelli visibili
@app.route('/replan', methods=['GET', 'POST'])
def replan():
    film_id = request.form.get('replanFilm')
    if film_id != 'Seleziona un film':   
        u = films.update().where(films.c.id == film_id).values(planned = True)
        conn.execute(u)
        flash(f"Film successfully replanned!")
    else:
        flash(f"Non è stato selezionato alcun film")
    return redirect(url_for('film'))



#Rimozione di un film da quelli pianificati
@app.route('/filmremove', methods=['GET', 'POST'])
def filmremove():
    film_id = request.form.get('removeFilm')   
    if film_id != 'Seleziona un film':   
        u = films.update().where(films.c.id == film_id).values(planned = False)
        conn.execute(u)
        flash(f"Film successfully removed from schedule!")
    else:
        flash(f"Non è stato selezionato alcun film")
    return redirect(url_for('film'))   


#Sezione per la registrazione dei biglietti acquistati
@app.route('/buyticket', methods=['GET','POST'])
def buyticket():    
    if request.method == 'POST':
        #logging.error(request.get_json(silent=False))
        r = request.get_json()
        q = select([times]).\
            where((times.c.id == session['orario'])) 
        t = conn.execute(q).fetchone()        
        if session['role'] == 'moderator':
            price_pt = 0
        elif session['role'] == 'student':
            price_pt = 5.50
        else:
            price_pt = 10.00
        ins = tickets.insert()
        for i in r['selectedTickets']:
            conn.execute(ins,
               {'row':i[0], 'seat':i[1:], 'price':price_pt, 'cinema_id':1, 'time_id':t[0], 'user_id':session['user_id'], 'film_id':t[4]}
            )
        tot = price_pt*len(r['selectedTickets'])
        return str(tot)
    else:
        price = request.args.get("price")
        return render_template('buyticket.html', user=session['user'], price=price) 


#Funzione per eliminare il proprio account
@app.route('/deleteaccount')
def deleteaccount():
    d = users.delete().where(users.c.id == session['user_id'])
    conn.execute(d)
    flash(f"Il tuo account è stato eliminato!")
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("role", None)
    session.pop("filmdate", None)
    session.pop("category", None)
    return redirect(url_for('home'))


#assegnazione di un ruolo da parte di un moderatore
@app.route('/grantrole', methods=['GET','POST'])
def grantrole():
    if request.method == 'POST':
        u_id = request.form.get('grantRole')
        r = request.form.get('role')
        if u_id != 'Seleziona un utente':
            if r != 'Seleziona un ruolo':
                q = select([roles.c.user_id, roles.c.role]).where(roles.c.user_id == u_id)
                check = conn.execute(q).fetchone()
                if check:
                    if r == check[1]:
                        flash(f"L'utente {u_id} possiede già il ruolo {r}")
                    else:
                        u = roles.update().where(roles.c.user_id == u_id).values(role = r)
                        conn.execute(u)
                        flash(f"Ruolo aggiornato con successo all'utente {u_id}, ora è {r}")
                else:
                    ins = roles.insert()
                    conn.execute(ins,
                        {'user_id': u_id, 'role': r}
                    )
                    flash(f"Ruolo {r} assegnato con successo all'utente {u_id}")
            else:
                flash(f"Non è stato selezionato alcun ruolo")
        else:
            flash(f"Non è stato selezionato alcun utente")
        return redirect(url_for('user'))


#rimozione di un ruolo da parte di un moderatore
@app.route('/revokerole', methods=['GET','POST'])
def revokerole():
    if request.method == 'POST':
        u_id = request.form.get('revokeRole')
        if u_id != 'Seleziona un utente':
            d = roles.delete().where(roles.c.user_id == u_id)
            conn.execute(d)
            flash(f"Ruolo revocato correttamente")
        else:
            flash(f"Non è stato selezionato alcun utente")
    return redirect(url_for('user'))



if __name__=='__main__':
    app.run(debug=True)