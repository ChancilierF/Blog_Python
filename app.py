from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '@dmin13'

conn = sqlite3.connect('blogs_system.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

def create_table():
    query = '''CREATE TABLE IF NOT EXISTS tickets
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    blogtitle TEXT NOT NULL,
    blogbody TEXT NOT NULL,
    category TEXT,
    added_by TEXT NOT NULL)'''

    print("Creating table ...")
    cursor.execute(query)
    conn.commit()

create_table()




@app.route("/create_ticket", methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        blogtitle = request.form.get('blogtitle')
        blogbody = request.form.get('blogbody')
        category = request.form.get('category')
        added_by = request.form.get('added_by')
        
        query = '''INSERT INTO tickets 
        (blogtitle, blogbody, category, added_by) 
        VALUES (?, ?, ?, ?)'''
        cursor.execute(query, [blogtitle, blogbody, category, added_by]) 
        
        conn.commit()

    return render_template('/addblog.html')



@app.route('/')
def list_tickets():
    query = "SELECT * FROM tickets"
    cursor.execute(query)
    all_tickets = cursor.fetchall()

    return render_template('/index.html', all_tickets=all_tickets)


@app.route('/ticket_details/<int:ticket_id>')
def ticket_details(ticket_id):
    print(ticket_id)
    query = "SELECT * FROM tickets WHERE id = ?"
    cursor.execute(query, [ticket_id])
    ticket = cursor.fetchone()

    return render_template('/viewblog.html', ticket=ticket)


@app.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    if request.method == 'POST':
        blogtitle = request.form['blogtitle']
        blogbody = request.form['blogbody']
        category= request.form['category']
        added_by = request.form['added_by']
        
        query = '''UPDATE tickets
        SET blogtitle=?, blogbody=?, category=?, added_by=?
        WHERE id=?'''
        cursor.execute(query, [blogtitle, blogbody, category, added_by])
        conn.commit()
        return redirect(url_for('list_tickets'))

    query = "SELECT * FROM tickets WHERE id = ?"
    cursor.execute(query, [ticket_id])
    ticket = cursor.fetchone()
    return render_template('/update.html', ticket=ticket)


@app.route('/delete_ticket/<int:ticket_id>')
def delete_ticket(ticket_id):
    query = '''DELETE FROM tickets WHERE id =?'''
    cursor.execute(query, [ticket_id])
    conn.commit()
    return redirect(url_for('list_tickets'))

# Route to handle filtering
@app.route('/filter', methods=['GET'])
def filter_tickets():
    category = request.args.get('category')

    # Execute SQL query to filter tickets based on category
    cursor.execute("SELECT * FROM tickets WHERE category=?", (category,))   
    filtered_tickets = cursor.fetchall()

  

    return render_template('filter.html', filtered_tickets=filtered_tickets)



if __name__ == "__main__":
    app.run(debug=True)