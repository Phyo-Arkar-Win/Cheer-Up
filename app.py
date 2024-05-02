from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
con = sqlite3.connect('data.db', check_same_thread=False)
con.row_factory = sqlite3.Row

# Create Cursor
db = con.cursor()

# Route for log in page
@app.route('/login', methods=['GET', 'POST'])
def index():
    imageReference = 'Lisa Fotios from Pexels'
    if request.method == 'GET':
        if session:
            flash("You're already logged in.")
            return render_template('login.html', imageReference = imageReference)
        return render_template('login.html', imageReference = imageReference)

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check for user input validation
        if not username:
            flash('Empty username')
            return render_template('login.html', imageReference = imageReference)
        elif not password:
            flash('Empty Password')
            return render_template('login.html', imageReference = imageReference)

        db.execute('SELECT * FROM users WHERE username=?', [username])
        user = db.fetchall()
        if not user:
            flash("Invalid Username.")
            return render_template('login.html', imageReference = imageReference)
        elif not check_password_hash(user[0]['password'], password):
            flash('Invalid Username or Password.')
            return render_template('login.html', imageReference = imageReference)
        else:
            session.clear()
            session['user_id'] = user[0]['id']
            return redirect('/')
        

# Route for sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    imageReference = 'Toni Cuenca from Pexels'
    if request.method == 'POST':
        # Retrieve inputs from users
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        # Create a password hash
        hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        
        # For checking duplicate username
        db.execute('SELECT * FROM users WHERE username=(?)', [username])
        duplicationCheck = db.fetchall()
        
        # Check for input conditions
        if not name:
            flash('Empty Name') 
            return render_template('signup.html', imageReference = imageReference)
        elif not username:
            flash('Empty Username')
            return render_template('signup.html', imageReference = imageReference)
        elif not password:
            flash('Empty Password')
            return render_template('signup.html', imageReference = imageReference)
        elif not confirmation:
            flash('Empty Password Confirmation')
            return render_template('signup.html', imageReference = imageReference)
        elif password != confirmation:
            flash("Passwords don't match!")
            return render_template('signup.html', imageReference = imageReference)
        elif duplicationCheck:
            flash('Username already exists.')
            return render_template('signup.html', imageReference = imageReference)
        # Insert into users table
        else:
            db.execute('INSERT INTO users (name, username, password, requests) VALUES (?,?,?,?)', (name, username, hash, 0))
            con.commit()

            # Remembering users using session
            db.execute('SELECT * FROM users WHERE username=?', [username])
            user = db.fetchall()
            session.clear()
            session['user_id'] = user[0]['id']
            return redirect('/')

    else:
        return render_template('signup.html', imageReference = imageReference)


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    imageReference = "Stephan Seeber from Pexels"
    if request.method == 'POST':
        db.execute('SELECT * FROM users WHERE id=?', [session['user_id']])
        user = db.fetchall()
        userMood = request.form.get('moodSelector')
        action = request.form.get('action')
        
        # For Happy Mood Submissions
        if action == 'Submit':
            message = request.form.get('happyInput')
            recipientMood = request.form.get('recipientMood')
            # User input validation for happyDiv
            if message and recipientMood:
                db.execute('INSERT INTO messages (category, name, username, message, reports) VALUES (?, ?, ?, ?, ?)', (recipientMood, user[0]['name'], user[0]['username'], message, 0))
                con.commit()
                inputSuccess = True
                return render_template('index.html', user = user, userMood = userMood, inputSuccess = inputSuccess, imageReference = imageReference)
            elif not message or not recipientMood:
                happyError = True
                return render_template('index.html', user = user, happyError = happyError, imageReference = imageReference)

        # For Other Mood Submissions
        elif action == 'Cheer me up!':
            if userMood:
                db.execute('SELECT * FROM messages WHERE category = ? AND username != ?', (userMood, user[0]['username']))
                output = db.fetchall()
                # Error handling for running out of things to output(hopefully it won't happen)
                try:
                    num = random.randrange(0, len(output))
                except:
                    outOfMessages = True
                    return render_template('index.html', user = user, outOfMessages = outOfMessages, imageReference = imageReference)
                db.execute('UPDATE users SET requests=? WHERE id=?', ((user[0]['requests'] + 1), session['user_id']))
                con.commit()

                # If the user has requested 5 times
                if (user[0]['requests'] + 1) == 5:
                    askForInput = True
                    return render_template('index.html', user = user, sender = output[num] , userMood = userMood, output = output[num]['message'], askForInput = askForInput, imageReference = imageReference)

                return render_template('index.html', user = user, sender = output[num] , userMood = userMood, output = output[num]['message'], imageReference = imageReference)

        # For reports
        elif action == 'Report':
            db.execute('SELECT * FROM messages WHERE username=? and message=?', (request.form.get('reportedUser'), request.form.get('reportedMessage')))
            reportedMessage = db.fetchall()
            db.execute('UPDATE messages SET reports=? WHERE username=? AND message=?', ((reportedMessage[0]['reports'] + 1), reportedMessage[0]['username'], reportedMessage[0]['message']))
            con.commit()
            db.execute('SELECT * FROM messages WHERE username=? and message=?', (request.form.get('reportedUser'), request.form.get('reportedMessage')))
            reportedMessage = db.fetchall()
            if reportedMessage[0]['reports'] == 5:
                db.execute('INSERT INTO review (id, category, name, username, message, reports) VALUES (?, ?, ?, ?, ?, ?)',
                            (reportedMessage[0]['id'], reportedMessage[0]['category'], reportedMessage[0]['name'], reportedMessage[0]['username'], reportedMessage[0]['message'], reportedMessage[0]['reports']))
                con.commit()
                db.execute('DELETE FROM messages WHERE username=? AND message=?', (reportedMessage[0]['username'], reportedMessage[0]['message']))
                con.commit()
            reportSuccess = True
            return render_template('index.html', user = user, reportSuccess = reportSuccess, imageReference = imageReference)
            
        return render_template('index.html', user = user, userMood = userMood, imageReference = imageReference)

    elif request.method == 'GET':
        if(session):
            db.execute('SELECT * FROM users WHERE id=?', [session['user_id']])
            user = db.fetchall()
            return render_template('index.html', user = user, imageReference = imageReference)
        else:
            return redirect('/login')

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()
    logoutSuccess = True
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)