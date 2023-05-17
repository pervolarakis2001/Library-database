from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

class School(FlaskForm):
    id = IntegerField(label = "school_id", validators = [DataRequired(message = "School_id is a required field.")] )
    name = StringField(label = "name", validators = [DataRequired(message = "Name is a required field.")])
    adm = IntegerField(label = "admin_id", validators = [DataRequired(message = "admin_id is a required field.")] )
    op = IntegerField(label = "operator_id", validators = [DataRequired(message = "operator_id is a required field.")] )
    city = StringField(label = "city", validators = [DataRequired(message = "City is a required field.")])
    pos = StringField(label = "postcode", validators = [DataRequired(message = "Postal Code is a required field.")])
    email = StringField(label = "email", validators = [DataRequired(message = "email is a required field.")])
    prF= StringField(label = "pr_First_name", validators = [DataRequired(message = "First name of Primary is a required field.")])
    prL = StringField(label = "pr_Last_name", validators = [DataRequired(message = "Last name of Primary is a required field.")])

    submit = SubmitField("Create") 
      
    
class Operator_reg(FlaskForm):
        FirstName= StringField(label = "First_name", validators = [DataRequired(message = "First name is a required field.")])
        LastName = StringField(label = "Last_name", validators = [DataRequired(message = " Last name is a required field.")])
        email = StringField(label = "email", validators = [DataRequired(message = "email is a required field.")])
        username = StringField(label = "username", validators = [DataRequired(message = " username is a required field.")])
        password = StringField(label = "password", validators = [DataRequired(message = " password is a required field.")])
        School = StringField(label = "school", validators = [DataRequired(message = " Last name is a required field.")])
        user_type = StringField(label = "user_type", validators = [DataRequired(message = " user_typeis a required field.")])
        School_user = StringField(label = "school_user", validators = [Optional()])

class Operator_approve(FlaskForm):
        FirstName= StringField(label = "First_name", validators = [DataRequired(message = "First name is a required field.")])
        LastName = StringField(label = "Last_name", validators = [DataRequired(message = " Last name is a required field.")])
        email = StringField(label = "email", validators = [DataRequired(message = "email is a required field.")])
       
        School = StringField(label = "school", validators = [DataRequired(message = " Last name is a required field.")])
       

class Books(FlaskForm):
    isbn = StringField(label = "ISBN", validators = [DataRequired(message = "ISBN is a required field.")] )
    school_id = IntegerField(label = "school_id", validators = [DataRequired(message = "school_id is a required field.")])
    operator_id = IntegerField(label = "operator_id", validators = [DataRequired(message = "operator_id is a required field.")] )
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")] )
    publisher = StringField(label = "publisher", validators = [DataRequired(message = "publisher is a required field.")])
    num_of_pages = IntegerField(label = "num_of_pages ", validators = [DataRequired(message = "num_of_pages is a required field.")])
    avail_copies = IntegerField(label = "avail_copies", validators = [DataRequired(message = "avail_copies is a required field.")])
    language= StringField(label = "language", validators = [DataRequired(message = "Language is a required field.")])


    submit = SubmitField("Create")