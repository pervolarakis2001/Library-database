from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, abort
from flask_mysqldb import MySQL
from flask_login import login_user, login_required, logout_user, current_user
import MySQLdb.cursors
from Website import app, db  # initially created by __init__.py, need to be used here
from Website.model import *
import subprocess
from datetime import date
import json
import os

@app.route("/")
def index():
    return render_template("landing.html", pageTitle="Landing Page")

file_path = r'C:\Users\DELL\Desktop\Library\Website\retrieve.json'
file_path_2 = r'C:\Users\DELL\Desktop\Library\Website\status.json'
school_op = []  # dictionary to keep values of sign up forms
@app.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
      
        FirstName= request.form.get('FirstName')
        LastName = request.form.get('LastName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        School = request.form.get('School')
        age = request.form.get('age')
        user_type = request.form.get('user_type')
        status= "empty"
       
        if user_type==  "School_user":
            status = request.form.get('status')
        
        
    
        # Data Constraints 
       
        ######## if users data is null then flash("error")
        if len(FirstName) > 20 :
            flash("Fist Name must be less than 20 characters", category='error')
        elif len(LastName) > 20 :
            flash("Last Name must be less than 20 characters", category='error')
        elif len(email)<2 or len(email)> 60  :
            flash("Email must be greater that 2 and less than 50 characters", category= 'error')
        elif len(username) > 40 :
            flash("username must be less than 40 characters", category= 'error')
        elif len(password) > 15: 
            flash("password must be less than 15 characters", category= 'error')
        else: 
            #add user to database 
            if user_type == "operator":
                    with open(file_path, 'r') as file:
                # Load the existing data from the JSON file
                        existing_data = json.load(file)
   
                        new_data = {'school':School, 'status': status}

                        # Append the new data to the existing data
                        existing_data.append(new_data)

        
                    with open(file_path, 'w') as file:
                        # Write the updated data to the JSON file
                        json.dump(existing_data, file)
   
                    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                    
                    query = f"""
                    SELECT u.username,u.password  from users u inner join operator op on u.user_id=op.operator_id 
                    WHERE username='{username}'
                    and password='{password} and approved=TRUE'
                    """
                    cur.execute(query)                 
                    record_1 = cur.fetchone() 
                    
                    if record_1:
                        flash('operator allready exists',category='error')
                    else:
                        cur.execute("SELECT MAX(user_id) as user FROM users")
                        user_id = cur.fetchone()
                        
                        user_id = user_id['user']
                        user_id =  user_id + 1
                       
                        query = f"""
                        INSERT INTO users (user_id,First_name,Last_name,user_type,username,password,approved) VALUES ({user_id},'{FirstName}', '{LastName}','{user_type}','{username}','{password}',FALSE);

                        """
                        cur.execute(query)  
                        query = f"""
                            INSERT INTO email_table (email,user_id) VALUES ('{email}',{user_id});
                        """
                        cur.execute(query) 
                        query = f"""
                            INSERT INTO phone_table (phone_number,user_id) VALUES ('{phone}',{user_id});
                        """
                        
                        cur.execute(query) 
                        db.connection.commit()
                        flash('application form sent, please wait administrator to give permission for access',category='success')
                    cur.close()    

            elif  user_type == "School_user":
                    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                    #add user to database 

                    
                    # Check if the JSON file exists
                    if os.path.isfile(file_path_2) and os.path.getsize(file_path) > 0:

                        # File exists and is not empty
                        with open(file_path_2, 'r') as file:
                            # Load the existing data from the JSON file
                              try:
                                    # Load the existing data from the JSON file
                                    existing_data = json.load(file)
                              except json.decoder.JSONDecodeError:
            # Handle empty or invalid JSON file
                                    existing_data = []
                          
                    else:
                        # File is empty or does not exist
                        existing_data = []

                    new_data = {'school': School, 'status': status,'age':age}

                    # Append the new data to the existing data
                    existing_data.append(new_data)

                    with open(file_path_2, 'w') as file:
                        # Write the updated data to the JSON file
                        json.dump(existing_data, file)
   
                    query = f"""
                    SELECT u.username,u.password  from users u inner join operator op on u.user_id=op.operator_id 
                    WHERE username='{username}'
                    and password='{password} AND approved=TRUE'
                    """
                    cur.execute(query)                 
                    record_1 = cur.fetchone() 
                    
                    if record_1:
                        flash('operator allready exists',category='error')
                    else:
                        cur.execute("SELECT MAX(user_id) as user FROM users")
                        user_id = cur.fetchone()
                        
                        user_id = user_id['user']
                        user_id =  user_id + 1
                        
                        session['status_signup']= status
                        query = f"""
                            INSERT INTO users (user_id,First_name,Last_name,user_type,username,password,approved) VALUES ({user_id},'{FirstName}','{LastName}','school_users','{username}','{password}',FALSE);
                        """
                        cur.execute(query) 
                         
                        query = f"""
                            INSERT INTO email_table (email,user_id) VALUES ('{email}',{user_id});
                        """
                        cur.execute(query) 
                        query = f"""
                            INSERT INTO phone_table (phone_number,user_id) VALUES ('{phone}',{user_id});
                        """
                        
                        cur.execute(query)  
                        db.connection.commit()
                        flash('application form sent, please wait administrator to give permission for access',category='success')
                    cur.close()  
    return render_template("sign_up.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
         # Check if account exists using MySQL
       
        cur.execute('SELECT * FROM users WHERE username= %s AND password= %s and approved=TRUE',(username,password,))
        record = cur.fetchone() 
        cur.execute('select email from email_table e inner join users u on e.user_id= u.user_id WHERE username = %s  and approved=TRUE',(username,))
        record2 = cur.fetchone() 
        cur.execute('select phone_number from phone_table e inner join users u on e.user_id= u.user_id WHERE username = %s  and approved=TRUE',(username,))
        record6 = cur.fetchone() 
        cur.execute('select status from school_users e inner join users u on e.school_users_id= u.user_id WHERE username = %s  and approved=TRUE',(username,))
        record3 = cur.fetchone() 
        cur.execute('select s.name from school s inner join school_users sch on sch.school_id = s.school_id inner join users u on user_id = sch.school_users_id WHERE username = %s  and u.approved=TRUE',(username,))
        record4 = cur.fetchone() 
        cur.execute('select phone_number from phone_table p inner join users u on u.user_id = p.user_id where username  = %s  and approved=TRUE',(username,))
        record5 = cur.fetchone() 
        
          
        if record:
           
            if record['user_type']== 'admin':
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['user_id'] = record['user_id']
                session['username'] = record['username']
                session['First_name'] = record['First_name']
                session['Last_name'] = record['Last_name']
                session['user_type'] = record['user_type']
                flash("Logged in successfully !",category='success')
                return redirect(url_for('admin'))
            
            elif record['user_type']  == 'school_users':
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['user_id'] = record['user_id']
                session['username'] = record['username']
                session['First_name'] = record['First_name']
                session['Last_name'] = record['Last_name']
                session['user_type'] = record['user_type']
                session['status'] = record3['status']
                session['email'] = record2['email']
                session['phone'] = record6['phone_number']
                session['school'] = record4['name']
                session['phone'] = record5['phone_number']
               
                flash("Logged in successfully !",category='success')
                return redirect(url_for('school_users'))
            
            else:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['user_id'] = record['user_id']
                session['username'] = record['username']
                session['First_name'] = record['First_name']
                session['Last_name'] = record['Last_name']
                session['user_type'] = record['user_type']
                session['email'] = record2['email']
                session['phone'] = record6['phone_number']
                flash("Logged in successfully !",category='success')
                return redirect(url_for('operator'))
        else:
            flash("username or password is wrong, please try again", category="error")
        
        cur.close()
    return render_template("login.html")


@app.route("/admin",methods=['GET','POST'])
def admin():
     return render_template("admin.html")

@app.route('/logout')
def logout(): 
    session.clear()
    return redirect('/')

@app.route("/admin/schools", methods=['GET','POST'])
def admin_schools():
    
    cur = db.connection.cursor()
    form = School()
    query = """
    SELECT * FROM school
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    school = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()    
    return render_template("admin_schools.html", school=school , form=form )

@app.route("/admin/schools/add", methods=['GET','POST'])
def admin_schools_add():
    
    cur = db.connection.cursor()
    
    
    if(request.method == "POST"):        
        school_name= request.form.get('school_name')
        postcode= request.form.get('postcode')
        city = request.form.get('city')
        email = request.form.get('email')
        pr_First_name = request.form.get('pr_First_name')
        pr_Last_name = request.form.get('pr_Last_name')
        op_First_name = request.form.get('op_First_name')
        op_Last_name = request.form.get('op_Last_name')
        operator_id = request.form.get('operator_id')
        admin_id = 911900
        cur.execute("SELECT MAX(school_id) FROM school")
        id = str(cur.fetchall()[0][0]+1)
        
        admin_id = 9119000
        cur.execute('SELECT name FROM school WHERE name = %s ',(school_name,))
        record = cur.fetchone() 
        if record:
            flash("School already exists!",category= 'error')
        else:     
            query = f"""
            INSERT INTO school (school_id, admin_id, operator_id,name,postcode,city,email,pr_First_name,pr_Last_name) VALUES ({id},'{admin_id}','{operator_id}','{school_name}','{postcode}','{city}','{email}','{pr_First_name}','{pr_Last_name}')
            """
            
            cur.execute(query)
            db.connection.commit()
            cur.close()

            flash("School added successfully", category="success")
            return  redirect('/admin/schools')
            
    return render_template("school_add.html")


@app.route("/admin/requests", methods=['GET','POST'])
def admin_requests():
        with open(file_path, 'r') as file:
            data = json.load(file)
        
       
        cur = db.connection.cursor()
        query = f"""
        SELECT * FROM users u  inner join email_table e on e.user_id =u.user_id inner join phone_table p on p.user_id = e.user_id  WHERE approved = FALSE AND user_type='operator'
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        info_op = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print(info_op)
        cur.close()
       
        for i, dictionary in enumerate(info_op):
            if i < len(data):
                dictionary.update(data[i])
        
        return render_template("admin_requests.html", info_op=info_op)

@app.route('/accept_request', methods=['GET','POST'])
def accept_request():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        school = request.form['school']
        # we use email to find user's id because email is unique
        query = f"""
            Select user_id FROM email_table Where email='{email}'  
            """
        cur.execute(query)
        user_id = str(cur.fetchall()[0][0])
        
        query = f"""
              update users set approved = TRUE WHERE user_id ={user_id}; 
            """
        cur.execute(query)
        query = f"""
             INSERT INTO operator (operator_id,admin_id,user_type) VALUES ({user_id},9119000,'operator')
            """
        cur.execute(query)
        db.connection.commit()
        
        flash("operator accepted please add school of operator!",category="success")
        cur.close()
    return redirect('/admin/requests')

# Route to handle denying a request
@app.route('/deny_request', methods=['GET','POST'])
def deny_request():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
       
        school = request.form['school']
        phone = request.form['phone']
        query = f"""
            Select user_id FROM email_table Where email='{email}'  
            """
        cur.execute(query)
        user_id = str(cur.fetchall()[0][0])
        query = f"""
              delete FROM  email_table  WHERE email = '{email}';  
            """
        cur.execute(query)
        query = f"""
               delete FROM  phone_table  WHERE user_id ={user_id};
            """
        cur.execute(query)
        query = f"""
              delete FROM  users  WHERE user_id ={user_id};
            """
        cur.execute(query)
       
        db.connection.commit()
        cur.close()
        flash("operator denied",category="success")
        
   
    return redirect('/admin/requests')

@app.route("/operator",methods=['GET','POST'])
def operator():
    return render_template("operator.html")

@app.route("/operator/books",methods=['GET','POST'])
def operator_books():
    cur = db.connection.cursor()
    
    operator_id = session.get("user_id")
    form = Books()
    query = f"""
    SELECT * FROM books b  inner join author_table a on a.ISBN = b.ISBN inner join category_table c on c.ISBN = b.ISBN WHERE operator_id ='{operator_id}'
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    school = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    cur.close()
    return render_template("books.html",school=school ,form = form )


@app.route("/operator/book/add", methods=['GET','POST'])
def operator_book_add():
     
    cur = db.connection.cursor()


    if(request.method == "POST"):

        operator_id = session.get("user_id")          
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publisher = request.form.get('publisher')
        num_of_pages = request.form.get('num_of_pages')
        summary = request.form.get('summary')
        avail_copies = request.form.get('avail_copies')
        language = request.form.get('language')
        keywords = request.form.get('keywords')
        cur.execute('SELECT ISBN FROM books WHERE ISBN = %s ',(isbn,))
        record = cur.fetchone() 
        cur.execute('SELECT school_id FROM school WHERE operator_id = %s ',(operator_id,))
        school_id =  cur.fetchone()
        school_id = school_id[0]
        image = request.form.get('image')
       
        if record:
            flash("Book already exists!",category= 'error')
        else:
            query = f"""
            INSERT INTO books (ISBN, school_id,operator_id,title,publisher,num_of_pages,summary,avail_copies,language,image,keywords) VALUES ("{isbn}",{school_id},"{operator_id}","{title}","{publisher}",{num_of_pages},'{summary}',{avail_copies},'{language}','{image}','{keywords}')
            """
            cur.execute(query)
            data_1 = request.form.get('author')
            author = f"author = '{data_1}'  " if (data_1 != "") else ""

            data_2 = request.form.get('category')
            category = f"category = '{data_2}'  " if (data_2 != "") else ""

            auth = data_1

          
            auth=  data_1.split(',')
    
            for i in auth:
                
                my_query = (
                f"INSERT INTO author_table (ISBN, author) VALUES ('{isbn}','{i}')"
            )
                cur.execute(my_query)
                db.connection.commit()
            cat = data_2

        
            cat=  data_2.split(',')
        
            for i in cat:
                
                my_query = (
                f"INSERT INTO category_table (ISBN, category) VALUES ('{isbn}','{i}')"
            )
                cur.execute(my_query)
                db.connection.commit()
            
            
            flash("Book added successfully", category="success")
            return  redirect('/operator/books')
            
    return render_template("book_add.html")

@app.route("/operator/book/change1",methods=['GET','POST'])
def change_book_oper(): 
      if(request.method == "POST"):
         isbn = request.form.get('isbn')
         session['isbn_1'] = isbn
         author= request.form.get('author')
         session['author_1'] = author
         category= request.form.get('category')
         session['category'] = category
        
      return render_template("change_book.html")
@app.route("/operator/book/change", methods=['GET','POST'])
def operator_book_change():
    
    cur = db.connection.cursor()
    
    if(request.method == "POST"):
        operator_id = session.get("user_id")
        print(operator_id)
            
        data = request.form.get('isbn') 
        isbn = f"ISBN = '{data}'" if (data != "") else ""

        data = request.form.get('title')
        title = f"title = '{data}'" if (data != "") else ""

        data = request.form.get('publisher')
        publisher = f"publisher = '{data}'" if (data != "") else ""
        
        num_of_pages = request.form.get('num_of_pages')
        num_of_pages = f"num_of_pages = {data}" if (data != "") else "" 
        
        data = request.form.get('summary')
        summary = f"summary = '{data}'" if (data != "") else ""
        
        data =  request.form.get('avail_copies')
        avail_copies = f"avail_copies = {data}" if (data != "") else ""

        data = request.form.get('language')
        language = f"language = '{data}'" if (data != "") else ""

        data = request.form.get('keywords')
        keywords = f"keywords = '{data}'  " if (data != "") else ""

        

        data_1 = request.form.get('author')
        author = f"author = '{data_1}'  " if (data_1 != "") else ""

        data_2 = request.form.get('category')
        category = f"category = '{data_2}'  " if (data_2 != "") else ""

        
        additionalQuery = [
            isbn,
            title,
            publisher,
            num_of_pages,
            summary,
            avail_copies,
            language,
            keywords,
          
        ]

        additionalQuery = ",".join(list(filter(lambda i: i != "", additionalQuery)))
        auth = data_1

        if auth != "":
            auth=  data_1.split(',')
       
            for i in auth:
                
                my_query = (
                f"update author_table set "
                +  f"author= '{i}' "
                + f" where ISBN = '{session.get('isbn_1')}' and author= '{session.get('author_1')}' "
            )
                cur.execute(my_query)
                db.connection.commit()
        cat = data_2

        if cat!= "" :
            cat=  data_2.split(',')
        
            for i in cat:
                
                my_query = (
                f"update category_table set "
                +  f"category= '{i}' "
                + f" where ISBN = '{session.get('isbn_1')}' and category= '{session.get('category')}' "
            )
                cur.execute(my_query)
                db.connection.commit()
        
        if  additionalQuery != "":
            my_query = (
                f"update books set "
                + additionalQuery
                + f" where ISBN = '{session.get('isbn_1')}' and operator_id={operator_id};"
            )
            cur.execute(my_query)
            db.connection.commit()
            cur.close()
        flash("book changes saved!",category='success')
        return redirect('/operator/books')
    return render_template("change_book.html")

@app.route('/backup', methods=['GET','POST'])
def backup():
    cursor = db.connection.cursor()
    d_b = 'library'
       
        # Getting all the table names
    cursor.execute('SHOW TABLES;')
    table_names = []
    for record in cursor.fetchall():
        table_names.append(record[0])
    
    backup_dbname = 'library' + '_backup'
    try:
        cursor.execute(f'CREATE DATABASE {backup_dbname}')
    except:
        pass
    
    cursor.execute(f'USE {backup_dbname}')
    print('ok')
    for table_name in table_names:
        cursor.execute(
            f'CREATE TABLE {table_name} SELECT * FROM {d_b}.{table_name}')
    flash('backup of database created',category='success')
    return redirect('/admin')




@app.route('/restore', methods=['GET','POST'])
def restore():
    cursor = db.connection.cursor()
  
    d_b = 'library'
    backup_dbname = d_b + '_backup'
    try:
        # Drop the existing database
        cursor.execute(f"DROP DATABASE IF EXISTS {d_b}")
        # Create a new empty database
        cursor.execute(f"CREATE DATABASE {d_b}")
        # Switch to the new database
        cursor.execute(f"USE {d_b}")

        # Get the table names from the backup database
        cursor.execute(f"SHOW TABLES IN {backup_dbname}")
        table_names = [record[0] for record in cursor.fetchall()]

        # Restore each table from the backup to the new database
        for table_name in table_names:
            cursor.execute(f"CREATE TABLE {table_name} SELECT * FROM {backup_dbname}.{table_name}")

        flash('Restore Successful', category='success')
    except Exception as e:
        flash('Restore Failed', category='error')
        print(e)
    finally:
        cursor.close()
        
    flash('Restore Successful',category="success")
    return redirect('/admin')

@app.route("/school_users",methods=['GET','POST'])
def school_users():
    return render_template("school_users.html")

@app.route("/sch_user_profile",methods=['GET','POST'])
def sch_user_profile():
      
        usernmae = session.get("username")
        First_name = session.get("First_name")
        Last_name = session.get("Last_name")
        email = session.get('email')
        school = session.get('school')
        phone = session.get('phone')
        if session.get('status') ==  "student":
            return render_template("student_prof.html",session=session)
        else:
            return render_template("teacher_prof.html",session=session)
            
       

@app.route("/edit_profile",methods=['GET','POST'])
def edit_profile():
     
      cur = db.connection.cursor()
      if(request.method == "POST"):
        school_users_id = session.get("user_id")
        username = request.form.get('username')      
        data = request.form.get('username') 
        username= f"username = '{data}'" if (data != "") else ""

        data = request.form.get('First_name')
        First_name = f"First_name = '{data}'" if (data != "") else ""

        data = request.form.get('Last_name')
        Last_name = f"Last_name = '{data}'" if (data != "") else ""
        
        data = request.form.get('email')
        email = f"email = {data}" if (data != "") else "" 
        
        data = request.form.get('school')
        school = f"school = '{data}'" if (data != "") else ""

        data =  request.form.get('password')
        password = f"password = {data}" if (data != "") else ""
        
        data =  request.form.get('phone')
        phone = f"phone = {data}" if (data != "") else ""

        
        additionalQuery = [
           username,
           First_name,
            Last_name,
            email ,
            school,
            password,
            phone
        ]

        additionalQuery = ",".join(list(filter(lambda i: i != "", additionalQuery)))
        print(additionalQuery)
       
        if  additionalQuery != "":
            my_query = (
                f"update users set "
                + additionalQuery
                + f" where user_id = {school_users_id} ;"
            )
            cur.execute(my_query)
            db.connection.commit()
            cur.close()
        flash("user proflie changes saved!",category='success')
      return render_template("edit_prof.html")
      
      
@app.route("/change_profile",methods=['GET','POST'])
def change_profile():   
      return render_template("edit_prof.html")

@app.route("/find_book_user",methods=['GET','POST'])
def find_book_user():
       cur = db.connection.cursor()
       if(request.method == "POST"):           
            title = request.form.get('title')
            category = request.form.get('category')
            author = request.form.get('author')
            query = f"""
            SELECT b.isbn,b.title,b.publisher, b.num_of_pages, b.avail_copies, b.language, a.author, c.category FROM books b  inner join author_table a on a.ISBN = b.ISBN inner join school sch on sch.school_id = b.school_id 
            inner join category_table c on c.ISBN= b.ISBN 
            WHERE title ='{title}' AND category='{category}' AND author='{author}' AND name ='{session.get('school')}'
            """
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
            if cur.fetchall()  == None:
                flash("book not found",category="error")
            else:
                return render_template("school_users.html",books = books,searched = True)
            cur.close()
       return render_template("school_users.html")

    
@app.route("/select/book",methods=['GET','POST'])
def select_book(): 
       cur = db.connection.cursor()
       if(request.method == "POST"):  
            ISBN= request.form['isbn']
            session['isbn_rating']=ISBN
            query = f"""
            SELECT title from books WHERE ISBN='{ISBN}'
            """
            cur.execute(query) 
            column_names = [i[0] for i in cur.description]
            title = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            session['title']= title
            query = f"""
            SELECT image from books WHERE ISBN='{ISBN}'
            """
            cur.execute(query) 
            column_names = [i[0] for i in cur.description]
            image = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            session['image']=image
            query = f"""
            SELECT summary from books WHERE ISBN='{ISBN}'
            """
            cur.execute(query) 
            column_names = [i[0] for i in cur.description]
            summary = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            session['summary']= summary
            query = f"""
            SELECT avg(rating_score) from ratings WHERE ISBN='{ISBN}'
            """
            cur.execute(query) 
            column_names = [i[0] for i in cur.description]
            rating = cur.fetchone()[0]
           
            query = f"""
            SELECT comments from ratings WHERE ISBN='{ISBN}' and approved=TRUE
            """
            cur.execute(query) 
            column_names = [i[0] for i in cur.description]
            comments = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            return render_template("select_book.html",image=image,title=title,summary =summary,rating=rating,comments= comments)
       return render_template("select_book.html")

inf_rat=[]
@app.route("/rating/book",methods=['GET','POST'])
def rate_book(): 
    cur = db.connection.cursor()
    rating = request.form.get('rating')
    comments = request.form.get('comment')
    if(request.method == "POST"):  
        
        cur.execute("SELECT MAX(rating_id) FROM ratings")
        rating_id = str(cur.fetchall()[0][0]+1)
        ISBN = session.get('isbn_rating')
        query = f"""
            SELECT operator_id FROM school_users where school_users_id = {session.get('user_id')}
            """
        cur.execute(query)
       
        operator_id = cur.fetchone()
        
        operator_id =operator_id[0]
        session['operator_id']= operator_id
        if session['status']== 'student':
            # senf request to operator to verify comment
            query = f"""
            INSERT INTO ratings (rating_id,ISBN,operator_id,school_users_id,comments,rating_score,approved) VALUES ({rating_id},'{ISBN}',{session.get('operator_id')},{session.get('user_id')},'{comments}','{rating}',FALSE);
            """
            cur.execute(query) 
            db.connection.commit()
            flash('your comment saved and will be published after verification of your operator',category='sucess')

        elif session['status'] == 'teacher':          
            query = f"""
            INSERT INTO ratings (rating_id,ISBN,operator_id,school_users_id,comments,rating_score,approved) VALUES ({rating_id},'{ISBN}',{session.get('operator_id')},{session.get('user_id')},'{comments}','{rating}',TRUE);
            """
            print('ok')
            cur.execute(query) 
            db.connection.commit()
            cur.close()
            flash('comment published successfuly',category='success')
    return redirect("/select/book")

    

@app.route("/rating/request",methods=['GET','POST'])
def rate_request(): 
    cur = db.connection.cursor()
    
    query = f"""
            SELECT  ISBN,school_users_id,comments FROM ratings WHERE operator_id={session.get('user_id')} AND approved=FALSE
            """
    cur.execute(query) 
    column_names = [i[0] for i in cur.description]
    inf_rat = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    return  render_template("rating_request.html",inf_rat=inf_rat)

@app.route("/publish_rating",methods=['GET','POST'])
def publish_request(): 
    cur = db.connection.cursor()
    if(request.method == "POST"):
        isbn= request.form['isbn']
        student_id=request.form['student_id']
        comments = request.form['comments']
        print(student_id)
      
        query = f"""
            update ratings set approved=TRUE WHERE ISBN ='{isbn}' AND school_users_id ={student_id}
            """
        cur.execute(query)
        db.connection.commit()
        
        flash(" comment published!",category="success")
        cur.close()
    return redirect('/rating/request')
    

@app.route("/deny_rating", methods=['GET','POST'])
def deny_request2(): 
    cur = db.connection.cursor()

    if(request.method == "POST"):

        isbn= request.form['isbn']
        student_id=request.form['student_id']
       
        comments = request.form['comments']
        query = f"""
            DELETE FROM  ratings  WHERE ISBN ='{isbn}' AND school_users_id = {student_id}
            """
        cur.execute(query)
        db.connection.commit()
        
        flash("comment deleted!",category="success")
        cur.close()
      
    return redirect("/rating/request")

@app.route("/user_reservations", methods=['GET','POST'])
def user_reservations(): 
    cur = db.connection.cursor()
    
    if(request.method == "POST"):  
        
        cur.execute("SELECT MAX(reservation_id) FROM reservations")
        a =cur.fetchone()
        if a[0] is  None:
            reservation_id = 1
            
        else:
           reservation_id = str(a[0]+1)
           
        isbn= request.form.get('isbn')
        title = request.form.get('title')
        reservation_date = date.today()
        school_users_id = session.get('user_id')
        query = f"""
            SELECT operator_id FROM school_users where school_users_id = {session.get('user_id')}
            """
        cur.execute(query)
        operator_id = cur.fetchone()
        operator_id =operator_id[0]
        print('ok')
        try:
            # Perform database operations
            query = f"""
            INSERT INTO reservations (ISBN,reservation_id,reservation_date,waiting,cancels,school_users_id,operator_id)  VALUES ('{isbn}',{reservation_id},'{reservation_date}',FALSE,FALSE,{school_users_id},{operator_id})
            """
            cur.execute(query)
            db.connection.commit()
            query = f"""
                        SELECT reservation_id,isbn,reservation_date,school_users_id FROM reservations WHERE school_users_id={school_users_id}
                        """
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            db.connection.commit()
            cur.close()
            print(reserve)
            flash('reservation submited',category='success')
            return redirect("/find_book_user")
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
           
    return redirect("/find_book_user")
    


@app.route("/trash_request", methods=['GET','POST'])
def trash_request(): 
    cur = db.connection.cursor()
    
    if(request.method == "POST"):  
        reservation_id = request.form.get('reservation_id')
        isbn= request.form.get('isbn')
        title = request.form.get('title')
        reservation_date = date.today()
        school_users_id = session.get('user_id')
        query = f"""
                DELETE FROM reservations WHERE reservation_id ={reservation_id}
                """
        cur.execute(query)
        db.connection.commit()
    return redirect("/user/resevations/btn")

@app.route("/user/resevations/btn", methods=['GET','POST'])
def reservations_users(): 
    cur = db.connection.cursor()
     
    query = f"""
                SELECT r.reservation_id,r.ISBN,r.reservation_date,r.school_users_id , a.title FROM reservations r INNER join books a
                    on r.ISBN= a.ISBN WHERE school_users_id={session.get('user_id')} 
                """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
   
    return  render_template("user_reservations.html",reserve=reserve)

@app.route("/operator/Reservations", methods=['GET','POST'])
def operator_reservations(): 
    cur = db.connection.cursor()
    print(session.get('user_id'))
    query = f"""
                SELECT r.reservation_id,r.ISBN,r.reservation_date,r.school_users_id , a.title FROM reservations r INNER join books a
                    on r.ISBN= a.ISBN WHERE r.operator_id ={session.get('user_id')}
                """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    return  render_template("operator_reservations.html",reserve=reserve)

@app.route("/approve/reservation", methods=['GET','POST'])
def operator_reservations_approve(): 
    cur = db.connection.cursor()
    if(request.method == "POST"):  
        cur.execute("SELECT MAX(borrowed_id) FROM borrowings")
        a =cur.fetchone()
        if a[0] is  None:
            borrowed_id = 1
            
        else:
           borrowed_id = str(a[0]+1)
           
        isbn= request.form.get('isbn')
        reservation_id= request.form.get('reservation_id')
        borrowing_date = date.today()
        operator_id = session.get('user_id')
        school_users_id = request.form.get('school_users_id')

      
        try:
            # Perform database operations
            query = f"""
                INSERT INTO borrowings (ISBN,operator_id,borrowed_id,school_users_id,borrowing_date,due_date,return_date) VALUES ('{isbn}',{operator_id},{borrowed_id},{school_users_id},'{borrowing_date}',NULL,NULL);
            """
            cur.execute(query)
            db.connection.commit()
            query = f"""
                 DELETE from reservations WHERE reservation_id={reservation_id};
            """
            cur.execute(query)
            db.connection.commit()
           
            flash('borrowing submited',category='success')
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
           
   
    return redirect('/operator/Reservations')

@app.route("/deny_borrowing", methods=['GET','POST'])
def deny_borrowing(): 
    cur = db.connection.cursor()
    
    if(request.method == "POST"):  
        reservation_id = request.form.get('reservation_id')
        
        query = f"""
                DELETE from reservations WHERE reservation_id={reservation_id};
                """
        cur.execute(query)
        db.connection.commit()
    return redirect('/operator/Reservations')

@app.route("/operator/borrowings", methods=['GET','POST'])
def operator_borrowings(): 
    cur = db.connection.cursor()
    operator_id = session.get('user_id')
    query = f"""
                SELECT * FROM borrowings WHERE operator_id={operator_id}
                """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    return  render_template("borrowings_op.html",reserve=reserve)

@app.route("/late_returns", methods=['GET','POST'])
def late_returns(): 
    cur = db.connection.cursor()
    if(request.method == "POST"):  

        operator_id = session.get('user_id')
        FirstName = request.form.get('FirstName')
        LastName = request.form.get('LastName')
        late_days = request.form.get('late_days')
        query = f"""
                SELECT * FROM borrowings b INNER JOIN users u on  u.user_id =b.school_users_id   where return_date is NULL AND b.operator_id={operator_id}
                AND u.First_name='{FirstName }' and  u.Last_name='{LastName}' AND DATEDIFF(curdate(),b.due_date) = '{late_days}'
                """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        if cur.fetchall()  == None:
                flash("book not found",category="error")
               
               
        else:
            return  render_template("late_returns.html",reserve=reserve,searched=True)

    return  render_template("late_returns.html")

@app.route("/school/user/Borrowings", methods=['GET','POST'])
def schusers_borrowings(): 
    cur = db.connection.cursor()
    
    query = f"""
                SELECT * FROM borrowings WHERE school_users_id={session.get('user_id')}

                """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    return  render_template("sch_user_borrowings.html",reserve=reserve)

@app.route("/waitings_reserve", methods=['GET','POST'])
def waitings_reserve(): 
    cur = db.connection.cursor()
    if(request.method == "POST"): 
        reservation_id = request.form.get('reservation_id')
        query = f"""
                    update reservations set waiting= TRUE Where reservation_id = {reservation_id}
                """
        cur.execute(query)
        db.connection.commit()
        flash("reservation went to waitings !", category="success")
       
    return redirect('/operator/Reservations')

@app.route("/waitings", methods=['GET','POST'])
def waitings(): 
    cur = db.connection.cursor()
     
    query = f"""
                Select * from reservations r inner join books b on r.ISBN=b.ISBN where waiting = TRUE
            """
    cur.execute(query)
  
    column_names = [i[0] for i in cur.description]
    reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    return render_template('waitings.html',reserve=reserve)
   

@app.route("/find_book_op",methods=['GET','POST'])
def find_book_operator():
       cur = db.connection.cursor()
       if(request.method == "POST"):           
            title = request.form.get('title')
            category = request.form.get('category')
            author = request.form.get('author')
            avail_copies = request.form.get('avail_copies')
            query = f"""
            SELECT b.isbn,b.title,b.publisher, b.num_of_pages, b.avail_copies, b.language, a.author, c.category FROM books b  inner join author_table a on a.ISBN = b.ISBN inner join school sch on sch.school_id = b.school_id 
            inner join category_table c on c.ISBN= b.ISBN 
            WHERE title ='{title}' AND category='{category}' AND author='{author}' AND avail_copies = {avail_copies} AND b.operator_id ='{session.get('user_id')}'
            """
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
            if cur.fetchall()  == None:
                flash("book not found",category="error")
            else:
                 return  render_template("books.html",books= books,searched=True)
            cur.close()
       return  render_template("books.html",books= books,searched=True)

@app.route("/find_rating_op",methods=['GET','POST'])
def find_rating_operator():
       cur = db.connection.cursor()
       if(request.method == "POST"):           
            sch_user_id = request.form.get('user_id')
            category = request.form.get('category')
            print(sch_user_id)
            query = f"""
           select avg(rating_score) as score,school_users_id,category from ratings r INNER JOIN category_table c  on c.Isbn = r.ISBN WHERE 
             r.school_users_id = {sch_user_id} and c.category = '{category}'
             
             """
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            print(books)
            cur.close()
            if cur.fetchall()  == None:
                flash("This user has not rate this category",category="error")
            else:
                return  render_template("rating_request.html",books= books,searched=True)           
               
       return  render_template("rating_request.html",books= books,searched=True)


@app.route("/bor_admin",methods=['GET','POST'])
def bor_admin_1():
        
        return render_template('borr_admin.html')
       
      
@app.route("/bor_admin/serch",methods=['GET','POST'])
def bor_admin():
        cur = db.connection.cursor()
        if(request.method == "POST"): 
            month = request.form.get('month')  
            year= request.form.get('year') 
            query = f"""
                        select sch.name as school, count(borrowed_id) as count from borrowings bor 
                        INNER JOIN operator op ON bor.operator_id = op.operator_id 
                        INNER JOIN school sch ON  sch.operator_id = op.operator_id WHERE MONTH(borrowing_date) ='{month}' AND YEAR(borrowing_date) ='{year}'
                        GROUP BY sch.name;
                    """
            cur.execute(query)
        
            column_names = [i[0] for i in cur.description]
            reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
        return  render_template("borr_admin.html",reserve=reserve,searched=True)

@app.route("/auth_cat_adm",methods=['GET','POST'])
def auth_cat_adm():
        
        return render_template('authcat_bor.html')

@app.route("/authcat_admin/search",methods=['GET','POST'])
def auth_cat_adm_search():
        cur = db.connection.cursor()
        if(request.method == "POST"): 
            category = request.form.get('category')  
            
            query = f"""
                        SELECT  category, us.First_name, us.Last_name FROM books b 
                        INNER JOIN category_table ct ON b.ISBN = ct.ISBN
                        INNER JOIN borrowings bor ON bor.ISBN = ct.ISBN
                        INNER JOIN school_users schu ON bor.school_users_id = schu.school_users_id
                        INNER JOIN users us ON us.user_id = schu.school_users_id
                        WHERE schu.status = "teacher" AND borrowing_date > DATE_ADD(curdate(),interval -1 year) 
                         AND category='{category}' ;   
                    """
            cur.execute(query)
        
            column_names = [i[0] for i in cur.description]
            reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            if len(reserve)== 0:
                flash("None of teacher has borrowed this category ",category='error')
            query = f"""
                        SELECT ct.category, author FROM books b 
                        INNER JOIN category_table ct ON b.ISBN = ct.ISBN
                        LEFT JOIN author_table aut ON ct.ISBN = aut.ISBN
                        WHERE category='{category}' ;   
                    """
            cur.execute(query)
        
            column_names = [i[0] for i in cur.description]
            reserve_2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
        return  render_template("authcat_bor.html",reserve=reserve,reserve_2=reserve_2,searched=True)

@app.route("/vew_young_teach",methods=['GET','POST'])
def vew_young_teach_1():
         cur = db.connection.cursor()
         query = f"""
               SELECT subquery.First_name, subquery.Last_name, MAX(subquery.borrow_count) AS max_borrow_count
                FROM (
                SELECT schu.school_users_id, us.First_name, us.Last_name, COUNT(bor.borrowed_id) AS borrow_count
                FROM books b
                INNER JOIN borrowings bor ON bor.ISBN = b.ISBN
                INNER JOIN school_users schu ON bor.school_users_id = schu.school_users_id
                INNER JOIN users us ON us.user_id = schu.school_users_id
                WHERE YEAR(CURDATE()) - DATE_FORMAT(schu.age, "%Y") < 40 
                    AND schu.status = "teacher"
                GROUP BY schu.school_users_id, us.First_name, us.Last_name
                ) AS subquery
                GROUP BY subquery.First_name, subquery.Last_name; 
                    """
         cur.execute(query)
    
         column_names = [i[0] for i in cur.description]
         reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
         return render_template('v_y_t_admin.html',reserve=reserve)
       
      
@app.route("/auth_no_bor",methods=['GET','POST'])
def auth_no_bor():
         cur = db.connection.cursor()
         query = f"""
                    select distinct aut.author from author_table aut
                    LEFT JOIN borrowings bor ON bor.ISBN = aut.ISBN
                    WHERE not exists (select 1 from borrowings inner join author_table aut1 on bor.ISBN = aut1.ISBN );
                    """
         cur.execute(query)
    
         column_names = [i[0] for i in cur.description]
         reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
         return render_template('auth_no_bor.html',reserve=reserve)

@app.route("/op_bor_same",methods=['GET','POST'])
def  op_bor_same():
         cur = db.connection.cursor()
         query = f"""
                   select op.operator_id, us.First_name, us.Last_name,count(bor.borrowed_id) as count from users us
                    inner join operator op on op.operator_id = us.user_id
                    inner join borrowings bor on bor.operator_id = op.operator_id  
                    inner join operator op1 on op1.operator_id = op.operator_id WHERE YEAR(bor.borrowing_date) IN (
                        SELECT DISTINCT YEAR(borrowing_date)
                        FROM borrowings
                    )
                    group by bor.operator_id 
                    having count(bor.borrowed_id) > 20 ;  
                    """
         cur.execute(query)
    
         column_names = [i[0] for i in cur.description]
         reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
         return render_template('auth_no_bor.html',reserve=reserve)


@app.route("/top_categories",methods=['GET','POST'])
def  top_categories():
         cur = db.connection.cursor()
         query = f"""
                    select ct1.category as cat1, ct2.category as cat2, count(bor.borrowed_id) as count from borrowings bor 
                    inner join books b on b.ISBN = bor.ISBN 
                    inner join category_table ct1 on ct1.ISBN = b.ISBN 
                    cross join category_table ct2 on ct1.category <> ct2.category  AND ct1.category < ct2.category AND ct1.ISBN = ct2.ISBN
                    group by ct1.category,ct2.category
                    limit 3;
                    """
         cur.execute(query)
    
         column_names = [i[0] for i in cur.description]
         reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
         return render_template('topcategories.html',reserve=reserve)


@app.route("/auth_5_books",methods=['GET','POST'])
def  auth_5_books():
         cur = db.connection.cursor()
         query = f"""
                   with aut_five_less_max (author,count_of_books_per_author) as
                    (select aut.author, count(b.ISBN) as count_of_books_per_author from books b 
                    inner join author_table aut on aut.ISBN = b.ISBN 
                    group by aut.author),
                    most_books_author (max_books_author) as
                    (select max(count_of_books_per_author) as max_books_author 
                    from aut_five_less_max)
                    select *
                    from aut_five_less_max aflm
                    join most_books_author mba 
                    on mba.max_books_author - 5 > aflm.count_of_books_per_author;
                    """
         cur.execute(query)
         column_names = [i[0] for i in cur.description]
         reserve = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
         return render_template('auth_5_book.html',reserve=reserve)

@app.route("/operator/requests",methods=['GET','POST'])
def  operator_requests():
        with open(file_path_2, 'r') as file:
            data = json.load(file)
        
       
        cur = db.connection.cursor()
        query = f"""
        SELECT * FROM users u  inner join email_table e on e.user_id =u.user_id inner join phone_table p on p.user_id = e.user_id  WHERE approved = FALSE AND user_type='school_users'
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        info_op = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
       
        cur.close()
       
        for i, dictionary in enumerate(info_op):
            if i < len(data):
                dictionary.update(data[i])
        flash('Thanks for signing up wait for your operator to give permission')
        return render_template("oper_requests.html", info_op=info_op)
@app.route('/accept_request_op', methods=['GET','POST'])
def accept_request_op():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        school = request.form['school']
        status = request.form['status']
        age = request.form['age']
        # we use email to find user's id because email is unique
        query = f"""
            Select user_id FROM email_table Where email='{email}'  
            """
        cur.execute(query)
        
        user_id = str(cur.fetchall()[0][0])
        query = f"""
            Select school_id FROM school Where operator_id ={session.get('user_id')} 
            """
        cur.execute(query)
        school_id = str(cur.fetchall()[0][0])
        query = f"""
              update users set approved = TRUE WHERE user_id ={user_id}; 
            """
        cur.execute(query)
        query = f"""
             INSERT INTO school_users (school_users_id,school_id,operator_id,age,status,user_type) VALUES ({user_id},{school_id},{session.get('user_id')},'{age}','{status}',"school_users");
            """
        cur.execute(query)
        db.connection.commit()
        
        flash("operator accepted !",category="success")
        cur.close()
    return redirect('/operator/requests')

@app.route('/deny_request_op', methods=['GET','POST'])
def deny_request_op():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
       
        school = request.form['school']
        phone = request.form['phone']
        query = f"""
            Select user_id FROM email_table Where email='{email}'  
            """
        cur.execute(query)
        user_id = str(cur.fetchall()[0][0])
        query = f"""
              delete FROM  email_table  WHERE email = '{email}';  
            """
        cur.execute(query)
        query = f"""
               delete FROM  phone_table  WHERE user_id ={user_id};
            """
        cur.execute(query)
        query = f"""
              delete FROM  users  WHERE user_id ={user_id};
            """
        cur.execute(query)
       
        db.connection.commit()
        cur.close()
        flash("operator denied",category="success")
        
   
    return redirect('/operator/requests')


@app.route("/vew_op",methods=['GET','POST'])
def  vewoperator():
        
       
        cur = db.connection.cursor()
        query = f"""
        SELECT * FROM operator op inner join users u on u.user_id = op.operator_id inner join school sc on op.operator_id = sc.operator_id
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        info_op = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
       
        cur.close()
       
        return render_template("vew_operators.html", info_op=info_op)


@app.route('/delete_op', methods=['GET','POST'])
def delete_op():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
       
        user_id = request.form['user_id']
        school = request.form['school']
        
        
        query = f"""
              delete FROM  email_table  WHERE user_id = {user_id};  
            """
        cur.execute(query)
        query = f"""
               delete FROM  phone_table  WHERE user_id ={user_id};
            """
        cur.execute(query)
        query = f"""
               delete FROM  operator  WHERE operator_id ={user_id};
            """
        cur.execute(query)
        query = f"""
              delete FROM  users  WHERE user_id ={user_id};
            """
        cur.execute(query)
       
        db.connection.commit()
        cur.close()
        flash("operator deleted",category="success")
        
   
    return redirect('/vew_op')


@app.route("/vew_memb",methods=['GET','POST'])
def  vew_operator():
        
       
        cur = db.connection.cursor()
        query = f"""
        SELECT * FROM school_users op inner join users u on u.user_id = op.school_users_id inner join school sc on op.operator_id = sc.operator_id where op.operator_id ={session.get('user_id')}
        """
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        info_op = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
      
        cur.close()
       
        return render_template("vew_members.html",info_op=info_op)

@app.route('/delete_sch_user', methods=['GET','POST'])
def delete_sch_usrr():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
       
        user_id = request.form['user_id']
        school = request.form['school']
        
        
        query = f"""
              delete FROM  email_table  WHERE user_id = {user_id};  
            """
        cur.execute(query)
        query = f"""
               delete FROM  phone_table  WHERE user_id ={user_id};
            """
        cur.execute(query)
        query = f"""
               delete FROM  school_users  WHERE school_users_id ={user_id};
            """
        cur.execute(query)
        query = f"""
              delete FROM  users  WHERE user_id ={user_id};
            """
        cur.execute(query)
       
        db.connection.commit()
        cur.close()
        flash("user deleted",category="success")
        
   
    return redirect('/vew_memb')


@app.route('/borrowing/add/man', methods=['GET','POST'])
def borrowingaddman():
    if(request.method == "POST"):
         isbn =request.form['isbn']
         session['isbn_man'] = isbn
       
    
    return render_template("add_bo_manualy.html")
@app.route('/borrowing/add/manually', methods=['GET','POST'])
def borrowingaddmanually():
    cur = db.connection.cursor()
    if(request.method == "POST"):
        
        isbn =session.get('isbn_man')
        print(isbn)
        id =  request.form['id']
        bor_day = date.today()
        cur.execute("SELECT MAX(borrowed_id) as user FROM borrowings")
        borrowed_id= cur.fetchone()
        print(isbn)
        borrowed_id =borrowed_id[0]
        borrowed_id =  borrowed_id + 1

        # Perform database operations
        query = f"""
        INSERT INTO borrowings (ISBN,operator_id,borrowed_id,school_users_id,borrowing_date,due_date,return_date) VALUES ('{isbn}',{session.get('user_id')},{borrowed_id},{id},'{bor_day}',NULL,NULL);
        """
        cur.execute(query)
        db.connection.commit()
        
        flash('borrowing submited',category='success')
    return render_template("add_bo_manualy.html")

@app.route('/delete_book', methods=['GET','POST'])
def delete_book():
    # Get the request details from the form data
    cur = db.connection.cursor()
    if(request.method == "POST"):
        ISBN = request.form['isbn']
        try:
            # Perform database operations
            query = f"""
                        DELETE FROM category_table where isbn = '{ISBN}'
                        """
            cur.execute(query)
          
            query = f"""
                        DELETE FROM author_table where isbn = '{ISBN}'
                        """
            cur.execute(query)
            query = f"""
                        DELETE FROM borrowings where isbn = '{ISBN}'
                        """
            cur.execute(query)
            query = f"""
                        DELETE FROM books where isbn = '{ISBN}'
                        """
            cur.execute(query)
            
            db.connection.commit()
            cur.close()
            
            flash('book deleted',category='success')
            
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
          
    return redirect('/operator/books')
        
@app.route('/activate_sch_user', methods=['GET','POST'])
def activate_user():
    cur = db.connection.cursor()
    if(request.method == "POST"):
         user_id = request.form.get('user_id')
         query = f"""
                 update users set approved = TRUE where user_id = {user_id}
                """
         cur.execute(query)
            
         db.connection.commit()
         flash('user activates',category='success')
         cur.close()
    return redirect('/vew_memb')

@app.route('/desable_sch_user', methods=['GET','POST'])
def desable_user():
   
    cur = db.connection.cursor()
    if(request.method == "POST"):
         user_id = request.form.get('user_id')
         query = f"""
                 update users set approved = FALSE where user_id = {user_id}
                """
         cur.execute(query)
            
         db.connection.commit()
         flash('user desabled',category='error')
         
    return redirect('/vew_memb')