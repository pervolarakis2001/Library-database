# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:28:59 2023

@author: DELL
"""


from collections import OrderedDict
import faker 
from datetime import datetime

import codecs
import random
import numpy as np


locales = OrderedDict([
    ('el-GR', 7),
    ('en-US', 2),
    ('el-CY', 4)
])
fake = faker.Faker(locales)



 ## public elements:
     
## NUMBER OF ENTITIES 
no_data = 200 

no_school = no_data//4
no_admin = 1
no_school_users = 100*no_school
no_operator = no_school
no_users = no_operator + no_school_users + no_admin
no_books = 200
no_borrowings = 50
no_reservations = 40
no_ratings = 15
## admin_ID
admin_id = 9119000
################## USERS ######################################
table_name = "users"
table_columns = ["user_id","First_name","Last_name","user_type"]
type = ["admin","operator","school_users"]
content = ""
users_id =[] 
j = 0 
for i in range(no_users):
    ID= 9119000 + i
    users_id.append(ID)
    firstName = fake.first_name()
    lastName = fake.last_name()
    if ID == 9119000:
        user_type = "admin"
    elif j <= no_operator:
        user_type="operator"
    else: 
        user_type = "school_users"
    j+=1
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ID}","{firstName}", "{lastName}","{user_type}");\n'
 
########################### admin ############################
table_name = "admin"
table_columns = ["admin_id","user_type"]


for i in range(no_admin):
    user_type = "admin"
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{admin_id}","{user_type}");\n'


   

################ operator ######################

table_name = "operator"
table_columns = ["operator_id","admin_id","user_type"]

op_id = []
for i in range(no_operator):
    operator_id =  9119000 + fake.unique.random_int(min=0, max=no_users - 1)
    op_id.append(operator_id)
    user_type = "operator"       
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{operator_id}","{admin_id}","{user_type}");\n'


list1 = [1,2,3,4]
list2 = [1,2]
s = set(list1)^set(list2)

########################## school ############################
 

table_name = "school"
table_columns = ["school_id","admin_id","name","postcode","city","email","pr_First_name","pr_Last_name","operator_id"]

s= ["Δημοτικό","Γυμνάσιο","Λύκειο"]


school_operator = {}

for i in range(no_school):
    sch_id = 1230 + i 
    name = random.choice(['1o ','2o ','3o ','4ο '])+ random.choice(s)+ " " + fake.city()
    postcode = fake.unique.postcode()
    city = fake.city()
    email = fake.unique.email()
    pr_First_name = fake.first_name()
    pr_LastName = fake.last_name()
    operator_id  = op_id[i]
    
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{sch_id}","{admin_id}","{name}","{postcode}","{city}","{email}","{pr_First_name}","{pr_LastName}","{operator_id}");\n'
    school_operator[operator_id] = sch_id

######################## school_users ####################

from faker import Faker

from datetime import datetime
f = Faker()
table_name = "school_users"
table_columns = ["school_users_id","school_id","operator_id","age","status","user_type"]
users_id_2 = users_id[0:no_operator+1]
s = set(users_id_2)^set(users_id)
school_users = list(s) ## school_users_id list.

schoolusers_operator = {}
for i in range(no_school_users):
    school_users_id = school_users[i]
    
    operator_id,school_id= random.choice(list(school_operator.items()))
   
    status = random.choice(["student","teacher"])
    if status == "student":
        age =  f.date_between_dates(date_start=datetime(2001,1,1), date_end=datetime(2019,1,1))
    else:
        age = f.date_between_dates(date_start=datetime(1965,1,1), date_end=datetime(1990,1,1))
    user_type = "school_users"
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{school_users_id}","{school_id}","{operator_id}","{age}","{status}","{user_type}");\n'
    schoolusers_operator[school_users_id] = operator_id

####################### books ##################################


lan = ["Ελληνικά","English","German","France"]
table_name = "books"
table_columns = ["ISBN","school_id","operator_id","title","publisher","num_of_pages",
                 "summary","avail_copies","language","image","keywords"]
isbn_operator = {}
for i in range(no_books):
    ISBN = fake.unique.isbn10()
    school_users_id = random.choice(school_users)
    operator_id,school_id = random.choice(list(school_operator.items()))
    title = fake.unique.text(max_nb_chars=20)
    publisher = fake.company()
    num_of_pages = fake.random_int(min=50, max=1500)
    summary = fake.paragraph(nb_sentences=10)
    avail_copies = random.choice([1,2,3,4,5,6,7,8,9,10])
    language = random.choice(lan)
  
    image = ""
    keywords= fake.text(max_nb_chars=15)
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{school_id}","{operator_id}","{title}","{publisher}","{num_of_pages}","{summary}","{avail_copies}","{language}","{image}","{keywords}");\n'
    isbn_operator[ISBN] = operator_id

    
################################### borrowigns ########################################################

table_name = "borrowings"
table_columns = ["ISBN","operator_id","borrowed_id","school_users_id","borrowing_date","due_date","return_date"]
from faker import Faker

from datetime import datetime

f = Faker()

borrowed_ISBN = {}
school_user_bor=[]
for i in range(no_borrowings):
    
    ISBN,operator_id= random.choice(list(isbn_operator.items()))
   
    borrowed_id = fake.ean(length=8)
    school_users_id = list(schoolusers_operator.keys())[list(schoolusers_operator.values()).index(operator_id)]
    if school_users_id in school_user_bor:
        i =i-1
        continue
    school_user_bor.append(school_users_id)
    borrwing_date = f.date_between_dates(date_start=datetime(2023,4,26), date_end=datetime(2023,4,26))
    due_date =f.date_between_dates(date_start=datetime(2023,5,3), date_end=datetime(2023,5,3))
    return_date = due_date
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{operator_id}","{borrowed_id}","{school_users_id}","{borrwing_date}","{due_date}","{return_date}");\n'
    borrowed_ISBN[ISBN] = operator_id 
    
    
##################### reservations #############################################

table_name = "reservations"
table_columns = ["ISBN","reservation_id","reservation_date","waiting","cancels","school_users_id","operator_id"]

 
res = borrowed_ISBN.items() & isbn_operator.items()


for i in range(no_reservations):
    school_users_id = list(schoolusers_operator.keys())[list(schoolusers_operator.values()).index(operator_id)]
    if school_users_id in school_user_bor:
        i = i -1
        continue 
    ISBN,operator_id= random.choice(list(res)) 
    reservation_id = 400 + fake.unique.random_int(min=0, max=no_reservations-1)
    reservation_date =  f.date_between_dates(date_start=datetime(2023,4,26), date_end=datetime(2023,5,3))
    waiting = random.choice([True,False])  
    cancels = random.choice([True,False]) 
  
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{reservation_id}","{reservation_date}",{waiting},{cancels},"{school_users_id}","{operator_id}");\n'
 
########### phone_table #################################

table_name = "phone_table"
table_columns = ["phone_number","user_id"]

 
res = borrowed_ISBN.items() & isbn_operator.items()

i=0
while i < no_users :
    if (random.uniform(0,1) <= 0.4): 
        i= i-1  
    phone_number = fake.unique.phone_number()
    user_id = users_id[i]
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{phone_number}","{user_id}");\n'
    i+=1
############################# ratings ########################################

table_name = "ratings"
table_columns = ["rating_id","ISBN","operator_id","school_users_id","comments","rating_score","approved"]

 
res = borrowed_ISBN.items() & isbn_operator.items()


for i in range(no_ratings):
       
    rating_id = 11000+ fake.unique.random_int(min=0, max=no_ratings-1)
    ISBN,operator_id = random.choice(list(isbn_operator.items()))
    school_users_id = list(schoolusers_operator.keys())[list(schoolusers_operator.values()).index(operator_id)]
    comments = fake.paragraph(nb_sentences=3)
    rating_score = random.choice(['1','2','3','4','5'])
    approved = random.choice([True,False]) 
    
    
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{rating_id}","{ISBN}","{operator_id}","{school_users_id}","{comments}","{rating_score}",{approved});\n'
    
###################### email_table #######################

table_name = "email_table"
table_columns = ["email","user_id"]


for i in range(no_users):
    if (random.uniform(0,1) <= 0.4): 
        i= i-1
    email = fake.unique.email()
    user_id = users_id[i]    
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{email}","{user_id}");\n'
    
 ################## category_table #################################
table_name = "category_table"
table_columns = ["ISBN","category"]
cat = ["Autobiography","Humor","Novels","Classics","Science Fiction","Poetry","History","Drama","Fairy tales","Horror","Crime","Fairy tale"]
i = 0 
h= 0 
isbn_category = {}
while i<no_books:  
    print(isbn_category)
    if (random.uniform(0,1) <= 0.4): 
        i= i-1
  
    ISBN,operator_id= list(isbn_operator.items())[i]
    category = random.choice(cat)
    if ISBN == list(isbn_category.keys())[list(isbn_category.values()).index(category)] and category in isbn_category :
        cat.remove(category)
        new_category = random.choice(cat)
        cat.append(category)
        category=new_category
        
    
    isbn_category[ISBN]=category   
    i+=1
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{category}");\n'

######################### author_table #################################
table_name = "author_table"
table_columns = ["ISBN","author"]

isbn_author = {}
i=0
while i < no_books:
    if (random.uniform(0,1) <= 0.4): 
        i= i-1
    
    ISBN,operator_id= list(isbn_operator.items())[i]
  
    author = fake.unique.name()
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1
f = open("dummy_data.txt", "w", encoding="utf-8")
f.write(content)
