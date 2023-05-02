
-- -----------------------------------------------------
-- Table "users"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users(
user_id INT UNSIGNED NOT NULL,
First_name VARCHAR(20) not null,
Last_name VARCHAR(20) not null,
user_type ENUM('admin','operator','school_users') NOT NULL,
primary key(user_id)
)ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table "admin"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS admin(
    admin_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (admin_id),
    user_type ENUM('admin') NOT NULL REFERENCES users(user_type),
    CONSTRAINT fk_admin_users
    FOREIGN KEY (admin_id) REFERENCES users (user_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "operator"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS operator (
	operator_id INT UNSIGNED NOT NULL,
    admin_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (operator_id),
    user_type ENUM('operator') NOT NULL REFERENCES users(user_type),
    CONSTRAINT fk_users_operator
    FOREIGN KEY (operator_id) REFERENCES users (user_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_admin_operator
    FOREIGN KEY (admin_id) REFERENCES admin (admin_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "school"
-- -----------------------------------------------------
create table IF NOT EXISTS school(
school_id INT UNSIGNED NOT NULL,
admin_id INT UNSIGNED NOT NULL,
name VARCHAR(60) NOT NULL,
postcode VARCHAR(40)  NOT NULL,
city VARCHAR(50) NOT NULL,
email VARCHAR(50) UNIQUE NOT NULL,
pr_First_name VARCHAR(50),
pr_Last_name VARCHAR(50),
operator_id INT UNSIGNED NOT NULL,
PRIMARY KEY (school_id),
CONSTRAINT fk_school_admin
FOREIGN KEY (admin_id) REFERENCES admin (admin_id)
 ON DELETE RESTRICT
ON UPDATE CASCADE,
CONSTRAINT fk_school_operator
FOREIGN KEY (operator_id) REFERENCES operator (operator_id)
 ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "school_users"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS school_users(
	school_users_id INT UNSIGNED NOT NULL,
    school_id INT UNSIGNED NOT NULL,
    operator_id INT UNSIGNED NOT NULL,
    age INT UNSIGNED NOT NULL,
    status VARCHAR(15),
    PRIMARY KEY (school_users_id),
    user_type ENUM('school_users') NOT NULL REFERENCES users(user_type),
    CHECK(status IN ('student','teacher')),
    CHECK( age<=18 AND age>7 AND status='student'),
	CHECK( age>18 AND status='teacher'),
    CONSTRAINT fk_users_school_users
    FOREIGN KEY (school_users_id) REFERENCES users (user_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_school_school_users
    FOREIGN KEY (school_id) REFERENCES school (school_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_operator_school_users
	FOREIGN KEY (operator_id) REFERENCES operator (operator_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE
)ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table "books"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS books (
    ISBN VARCHAR(40) PRIMARY KEY  NOT NULL,
    school_users_id INT UNSIGNED NOT NULL,
    school_id INT UNSIGNED NOT NULL,
    operator_id INT UNSIGNED NOT NULL,
    title VARCHAR(50) NOT NULL, 
    publisher VARCHAR(50) NOT NULL,
    num_of_pages INT NOT NULL,
    summary TEXT NOT NULL,
    avail_copies INT UNSIGNED,
    language VARCHAR(50) NOT NULL,
    image LONGBLOB,
    keywords VARCHAR(50) NOT NULL,
    CONSTRAINT fk_school_books
    FOREIGN KEY (school_id) REFERENCES school (school_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_admin_books
    FOREIGN KEY (operator_id) REFERENCES operator (operator_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
	CONSTRAINT fk_school_users_books
    FOREIGN KEY (school_users_id) REFERENCES school_users (school_users_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE
)ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table "authentification_system"
-- -----------------------------------------------------
create table IF NOT EXISTS  authentication_system(
login_id INT UNSIGNED NOT NULL,
user_id INT UNSIGNED NOT NULL,
username VARCHAR(20) NOT NULL,
password  VARCHAR(20) NOT NULL,
PRIMARY KEY (login_id),
CONSTRAINT fk_users_auths_system
FOREIGN KEY (user_id) REFERENCES users (user_id)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "borrowings"
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS borrowings(
ISBN VARCHAR(17) NOT NULL,
operator_id INT UNSIGNED NOT NULL,   
borrowed_id INT UNSIGNED NOT NULL,
school_users_id INT UNSIGNED NOT NULL,
borrowing_date DATE DEFAULT NULL,
due_date DATE NOT NULL,
return_date DATE DEFAULT NULL,
CHECK(borrowing_date<due_date),
PRIMARY KEY(borrowed_id),
CONSTRAINT fk_books_borrowings
FOREIGN KEY(ISBN) REFERENCES books(ISBN)
ON DELETE RESTRICT
ON UPDATE CASCADE,
CONSTRAINT fk_operator_borrrowings
FOREIGN KEY(operator_id) REFERENCES operator(operator_id)
ON DELETE RESTRICT
ON UPDATE CASCADE,
CONSTRAINT fk_school_users_borrowings
FOREIGN KEY(school_users_id) REFERENCES school_users(school_users_id)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "reservations"
-- -----------------------------------------------------

create table IF NOT EXISTS reservations(
ISBN VARCHAR(17) NOT NULL,
reservation_id INT UNSIGNED NOT NULL,
reservation_date  DATE DEFAULT NULL,
waiting BOOLEAN DEFAULT FALSE,
cancels BOOLEAN NOT NULL,
school_users_id INT UNSIGNED NOT NULL,
operator_id INT UNSIGNED NOT NULL,
CONSTRAINT fk_books_reservations
FOREIGN KEY(ISBN) REFERENCES books(ISBN)
ON DELETE RESTRICT
ON UPDATE CASCADE,
CONSTRAINT fk_operator_reservations
FOREIGN KEY(operator_id) REFERENCES operator(operator_id)
ON DELETE RESTRICT
ON UPDATE CASCADE,
CONSTRAINT fk_school_users_reservations
FOREIGN KEY(school_users_id) REFERENCES school_users(school_users_id)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table "phone_table"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS phone_table(
phone_number INT NOT NULL,
user_id INT UNSIGNED NOT NULL,
CONSTRAINT chk_phone CHECK (phone_Number RLIKE('[0-9]{10}')), 
PRIMARY KEY(user_id,phone_number),
CONSTRAINT fk_users_phone
FOREIGN KEY(user_id) REFERENCES users(user_id)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table "ratings"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ratings(
    rating_id INT UNSIGNED NOT NULL,
    ISBN VARCHAR(17) NOT NULL,
    operator_id INT UNSIGNED NOT NULL,
    school_users_id INT UNSIGNED NOT NULL,
    comments TEXT,
    rating_score VARCHAR(1) NOT NULL,
    approved BOOLEAN NOT NULL,
    PRIMARY KEY (rating_id),
     CHECK( rating_score in ('1','2','3','4','5')),
    CONSTRAINT fk_books_ratings
    FOREIGN KEY (ISBN) REFERENCES books (ISBN) 
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_operator_ratings
    FOREIGN KEY (operator_id) REFERENCES operator (operator_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
    CONSTRAINT fk_school_users_ratings
    FOREIGN KEY (school_users_id) REFERENCES school_users (school_users_id)
	ON DELETE RESTRICT
    ON UPDATE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS email_table(
email VARCHAR(30) NOT NULL,
user_id INT UNSIGNED NOT NULL,
PRIMARY KEY (email,user_id),
CONSTRAINT fk_users_email
FOREIGN KEY (user_id) REFERENCES users(user_id)
 ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table "category_table"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS category_table(
ISBN VARCHAR(17) NOT NULL,
category VARCHAR(50) NOT NULL,
PRIMARY KEY(ISBN,category),
CONSTRAINT fk_books_category
FOREIGN KEY(ISBN) REFERENCES books (ISBN)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table "author_table"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS author_table (
ISBN VARCHAR(17) NOT NULL,
author VARCHAR(50) NOT NULL,
CONSTRAINT books_author
FOREIGN KEY(ISBN) REFERENCES books (ISBN)
ON DELETE RESTRICT
ON UPDATE CASCADE
)ENGINE = InnoDB;




DELIMITER $
CREATE TRIGGER chk_reservations BEFORE INSERT ON reservations
FOR EACH ROW 
BEGIN 
	IF ( (SELECT s.school_users_id from school_users s INNER JOIN reservations r ON s.school_users_id=r.school_users_id 
    WHERE s.status='students' HAVING COUNT(r.school_users_id)=2) = new.school_users_id) AND  SELECT DATEDIFF(day,CURDATE(),new.reservation_date) < 7)
     SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on reservation failed - A student cannot make more than 2 reservations a week';
    END IF;
		

DELIMITER ;