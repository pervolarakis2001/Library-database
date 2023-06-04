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
no_data = 100 

no_school = 5
no_admin = 1
no_school_users = 50*no_school
no_operator = no_school
no_users = no_operator + no_school_users + no_admin
no_books = 100
no_borrowings = 50
no_reservations = 40
no_ratings = 15
## admin_ID
admin_id = 9119000
################## USERS ######################################
table_name = "users"
table_columns = ["user_id","First_name","Last_name","user_type","username","password","approved"]
type = ["admin","operator","school_users"]
content = ""
users_id =[] 
operators = []
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
        operators.append(ID)
    else: 
        user_type = "school_users"
    j+=1
    username = fake.unique.user_name()
    password = fake.nic_handle()
    
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ID}","{firstName}", "{lastName}","{user_type}","{username}","{password}",TRUE);\n'
 
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
    operator_id=operators[i]
    op_id.append(operator_id)
    user_type = "operator"       
 
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{operator_id}","{admin_id}","{user_type}");\n'


list1 = [1,2,3,4]
list2 = [1,2]
s = set(list1)^set(list2)

########################## school ############################
 

table_name = "school"
table_columns = ["school_id","admin_id","name","postcode","city","school_email","pr_First_name","pr_Last_name","operator_id"]

s= ["Δημοτικό","Γυμνάσιο","Λύκειο"]


school_operator = {}

for i in range(no_school):
    sch_id = 1230 + i 
    name = random.choice(['1o ','2o ','3o ','4ο'])+ random.choice(s)+ " " + fake.city()
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
oper_schoolusers={}
for i in range(no_school_users):
    school_users_id = school_users[i]
    
    operator_id,school_id= random.choice(list(school_operator.items()))
   
    status = random.choice(["student","teacher"])
    if status == "student":
        age =  f.date_between_dates(date_start=datetime(2001,1,1), date_end=datetime(2019,1,1))
    else:
        age = f.date_between_dates(date_start=datetime(1980,1,1), date_end=datetime(1995,1,1))
    user_type = "school_users"
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{school_users_id}","{school_id}","{operator_id}","{age}","{status}","{user_type}");\n'
    schoolusers_operator[school_users_id] = operator_id
    oper_schoolusers[operator_id]  = school_users_id
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
    image = "https://s26162.pcdn.co/wp-content/uploads/sites/3/2019/08/the-swallows-673x1024.jpg"
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
# seperate books per operator
op1=[]
op2=[]
op3=[]
op4=[]
op5=[]

for j in list(isbn_operator.items()):
    if j[1] == 9119001:
        op1.append(j)
    elif j[1]== 9119002:
        op2.append(j)
    elif j[1]== 9119003:
        op3.append(j)
    elif j[1]==9119004:
        op4.append(j)
    else:
        op5.append(j)
def get_keys_by_value(dictionary, value):
    return [key for key, val in dictionary.items() if val == value]

school_users_id_1 = get_keys_by_value(schoolusers_operator,9119001)
school_users_id_2 = get_keys_by_value(schoolusers_operator,9119002)
school_users_id_3 = get_keys_by_value(schoolusers_operator,9119003)
school_users_id_4 = get_keys_by_value(schoolusers_operator,9119004)
school_users_id_5 = get_keys_by_value(schoolusers_operator,9119005)


for i in range(no_borrowings//5):
    
    ISBN_1,operator_id_1= random.choice(op1)
    ISBN_2,operator_id_2= random.choice(op2)
    ISBN_3,operator_id_3= random.choice(op3)
    ISBN_4,operator_id_4= random.choice(op4)
    ISBN_5,operator_id_5= random.choice(op5)
  
    borrowed_id_1 = i +1
    borrowed_id_2 = i+11
    borrowed_id_3 = i +21
    borrowed_id_4 = i +31
    borrowed_id_5 = i +41
    school_users_1= school_users_id_1[i]
    school_users_2 = school_users_id_2[i]
    school_users_3 = school_users_id_3[i]
    school_users_4 = school_users_id_4[i]
    school_users_5 = school_users_id_5[i]
   
  

    school_user_bor.append(school_users_1)
    school_user_bor.append(school_users_2)
    school_user_bor.append(school_users_3)
    school_user_bor.append(school_users_4)
    school_user_bor.append(school_users_5)
   
    borrwing_date = f.date_between_dates(date_start=datetime(2023,3,3), date_end=datetime(2023,3,6))
    due_date = f.date_between_dates(date_start=datetime(2023,3,7), date_end=datetime(2023,3,15))
    return_date = due_date

    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN_1}","{operator_id_1}","{borrowed_id_1}","{school_users_1}","{borrwing_date}","{due_date}",NULL);\n'
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN_2}","{operator_id_2}","{borrowed_id_2}","{school_users_2}","{borrwing_date}","{due_date}","{return_date}");\n'
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN_3}","{operator_id_3}","{borrowed_id_3}","{school_users_3}","{borrwing_date}","{due_date}","{return_date}");\n'
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN_4}","{operator_id_4}","{borrowed_id_4}","{school_users_4}","{borrwing_date}","{due_date}","{return_date}");\n'
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN_5}","{operator_id_5}","{borrowed_id_5}","{school_users_5}","{borrwing_date}","{due_date}","{return_date}");\n'
   # borrowed_ISBN[ISBN] = operator_id 



for i in range(10):
    
    ISBN,operator_id= random.choice(op1)

    borrowed_id = 51+i
    school_users_id = school_users_id_1[i]
    
    borrwing_date = f.date_between_dates(date_start=datetime(2023,3,3), date_end=datetime(2023,3,6))
    due_date = f.date_between_dates(date_start=datetime(2023,3,7), date_end=datetime(2023,3,15))
    return_date = due_date
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{operator_id}","{borrowed_id}","{school_users_id}","{borrwing_date}","{due_date}","{return_date}");\n'
    borrowed_ISBN[ISBN] = operator_id 
    
for i in range(10):
    
    ISBN,operator_id= random.choice(op1)

    borrowed_id = 61+i
    school_users_id = school_users_id_4[i]
    
    borrwing_date = f.date_between_dates(date_start=datetime(2023,3,3), date_end=datetime(2023,3,6))
    due_date = f.date_between_dates(date_start=datetime(2023,3,7), date_end=datetime(2023,3,15))
    return_date = due_date
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{operator_id_1}","{borrowed_id}","{school_users_id}","{borrwing_date}","{due_date}","{return_date}");\n'
    borrowed_ISBN[ISBN] = operator_id 
    
##################### reservations #############################################

table_name = "reservations"
table_columns = ["ISBN","reservation_id","reservation_date","waiting","cancels","school_users_id","operator_id"]

 
for i in range(20,40):
  
    ISBN,operator_id= random.choice(op4) 
    school_users_id =  school_users_id_4[i]
    
    print(len(school_users_id_5))
       
    reservation_id = 400 + fake.unique.random_int(min=0, max=no_reservations-1)
    reservation_date =  f.date_between_dates(date_start=datetime(2023,4,6), date_end=datetime(2023,4,15))
    waiting = random.choice([True,False])  
    cancels = random.choice([False]) 
    
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{reservation_id}","{reservation_date}",{waiting},{cancels},"{school_users_id}","{operator_id}");\n'
        
    
 
########### phone_table #################################

table_name = "phone_table"
table_columns = ["phone_number","user_id"]

 
res = borrowed_ISBN.items() & isbn_operator.items()

i=0
while i < no_users :
   
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
    
    email = fake.unique.email()
    user_id = users_id[i]    
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{email}","{user_id}");\n'
    
 ################## category_table #################################

from faker import Faker

from datetime import datetime
f = Faker()
table_name = "category_table"
table_columns = ["ISBN","category"]
cat = ["Autobiography","Humor","Novels","Classics","Science Fiction","Poetry","History","Drama","Horror","Crime","Fairy tale"]

i = 0 
h= 0 
isbn_category = []
isv =[]
for i in range(no_books):  
    
  
  
    ISBN,operator_id= list(isbn_operator.items())[i]
    category =random.choice(cat)
   
  
   
  
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{category}");\n'
  
cat_2 = ["Arts & Photography","Biographies & Memoirs","Crafts","Health","Computers","Romance"]

for i in range(no_books//2):  
    
  
  
    ISBN,operator_id= list(isbn_operator.items())[i]
    category =random.choice(cat_2)
   
  
   
 
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{category}");\n'
    

cat_2 = ["Short stories","Woman Fiction"]
cat_3 = ["War","Young adult"]
for i in range(no_books//2):  
    
    ISBN,operator_id= list(isbn_operator.items())[i]
    category =random.choice(cat_2)
   
  
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{category}");\n'
  


for i in range(no_books//2):  
    
  
  
    ISBN,operator_id= list(isbn_operator.items())[i]
    category =random.choice(cat_3)
   
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{category}");\n'

######################### author_table #################################
table_name = "author_table"
table_columns = ["ISBN","author"]

isbn_author = {}
i=0
auth = "Makis Haralabithis"
while i < no_books:
    if (random.uniform(0,1) <= 0.4): 
        i= i-1
    
    ISBN,operator_id= list(isbn_operator.items())[i]
    author = fake.unique.name()
    
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1
i=0   
while i < no_books//4:
    
    
    ISBN,operator_id= list(isbn_operator.items())[i]
   
    
    author = auth
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1

auth = "Harry Styles"
i=0
while i < (no_books//4 -1):
    
    
    ISBN,operator_id= list(isbn_operator.items())[i]
   
    
    author = auth
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1
auth = "Harry Bob"
i=0
while i < (no_books//4 -2):
    
    
    ISBN,operator_id= list(isbn_operator.items())[i]
   
    
    author = auth
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1
auth = "Bob  Styles"
i=0
while i < (no_books//4 -2):
    
    
    ISBN,operator_id= list(isbn_operator.items())[i]
   
    
    author = auth
    content += f'INSERT INTO {table_name} ({",".join(table_columns)}) VALUES ("{ISBN}","{author}");\n'
    i+=1
    
f = open("dummy_data.txt", "w", encoding="utf-8")
f.write(content)
