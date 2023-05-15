-- ------------- TRIGGERS -------------------------------

-- Setting event to delete reservations after one week 
CREATE EVENT IF NOT EXISTS `delete_reservations_event`
ON SCHEDULE
  EVERY 1 DAY_HOUR 
  ON COMPLETION PRESERVE
  COMMENT 'Clean up reservations.'
  DO
    DELETE FROM reservations
    WHERE reservation_date < DATE_SUB(NOW(), INTERVAL 7 DAY)

-- ------------------ CHECK rules of  reservations   -------------------
DELIMITER $
CREATE TRIGGER chk_num_of_reservations BEFORE INSERT ON reservations
FOR EACH ROW 
BEGIN 
	IF (new.school_users_id = (SELECT r.school_users_id from reservations r INNER JOIN school_users s ON s.school_users_id = r.school_users_id INNER JOIN books b ON  b.ISBN = r.ISBN
    WHERE s.status = "student" AND r.ISBN = new.ISBN  GROUP BY r.school_users_id HAVING COUNT(*)= 2) AND DATEDIFF(new.reservation_date,CURDATE()) <7 ) THEN 
      SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on reservations failed - A student can only make 2 reservations a week.';
    END IF;
    IF (new.school_users_id = (SELECT r.school_users_id from reservations r INNER JOIN school_users s ON s.school_users_id = r.school_users_id INNER JOIN books b ON  b.ISBN = r.ISBN
    WHERE s.status = "teacher" AND r.ISBN = new.ISBN  GROUP BY r.school_users_id HAVING COUNT(*)= 1) AND DATEDIFF(new.reservation_date,CURDATE()) <=7)  THEN 
      SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on reservations failed - A teacher can only make 1 reservations a week.';
    END IF;
 IF(new.school_users_id = (select school_users_id from borrowings WHERE return_date IS NULL ) ) THEN 
 SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on reservations failed - A user cannot make reservation if a book has not been returned on time.';
    END IF;
IF (new.ISBN = (SELECT ISBN FROM borrowings   WHERE school_users_id =  new.school_users_id  AND return_date is null AND ISBN=new.ISBN) ) THEN
	SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on reservations failed - A user cannot make reservation if  if the same user has already borrowed the title.';
    END IF;
END$  
DELIMITER ; 

-- ------------------ CHECK rules of  borrowings   -------------------
DELIMITER $ 
CREATE TRIGGER chk_borrowings BEFORE INSERT ON borrowings
FOR EACH ROW 
BEGIN 
IF (new.school_users_id = (SELECT bor.school_users_id from borrowings bor INNER JOIN school_users s ON s.school_users_id = bor.school_users_id INNER JOIN books b ON  b.ISBN = bor.ISBN
    WHERE s.status = "student" AND bor.ISBN = new.ISBN  GROUP BY bor.school_users_id HAVING COUNT(*)= 2) AND DATEDIFF(new.borrowing_date,CURDATE()) <7 ) THEN 
      SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on  borrowings failed - A student can only borrow 2 books a week.';
    END IF;

IF (new.school_users_id = (SELECT bor.school_users_id from borrowings bor INNER JOIN school_users s ON s.school_users_id = bor.school_users_id INNER JOIN books b ON  b.ISBN = bor.ISBN
    WHERE s.status = "teacher" AND bor.ISBN = new.ISBN  GROUP BY bor.school_users_id HAVING COUNT(*)= 1) AND DATEDIFF(new.borrowing_date,CURDATE()) <7 ) THEN 
      SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on  borrowings failed - A teacher can only borrow 1 book a week.';
    END IF;
    
IF (new.school_users_id = (SELECT school_users_id from borrowings WHERE return_date is null AND ISBN = new.ISBN) AND DATEDIFF(new.borrowing_date,CURDATE()) > 7 ) THEN
	 SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on  borrowings failed - A user cannot borrow a book  if returns are delayed or still open.';
	 END IF;
     
IF (new.ISBN = (SELECT ISBN FROM books WHERE avail_copies = 0 AND ISBN = new.ISBN)) THEN
	 SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'check constraint on  borrowings failed - A user cannot borrow a book  if there is no  available copie of book.';
	 END IF;
END$ 
DELIMITER ; 



-- ---------------decrease available copies of a book when it gets borrowed and increae it when it gets returned --------------------------------------
DELIMITER $ 
CREATE TRIGGER decrease_avail_copies AFTER INSERT ON borrowings
FOR EACH ROW 
BEGIN 
	IF (new.return_date IS NULL) THEN 
		UPDATE books b SET b.avail_copies = b.avail_copies -1 WHERE ISBN = NEW.ISBN;
	 ELSEIF (new.return_date IS NOT NULL) THEN 
		UPDATE books b SET b.avail_copies = b.avail_copies +1 WHERE ISBN = NEW.ISBN;
	END IF;

END$ 
DELIMITER ; 

-- ----------- due date is a week after borrowing_date ------------------------
DELIMITER $ 
CREATE TRIGGER chk_due_date  BEFORE INSERT ON borrowings
FOR EACH ROW 
BEGIN 
	IF (new.return_date IS NULL) THEN 
		 SET NEW.due_date = date_add(new.borrowing_date,INTERVAL 7 DAY);	
	END IF;

END$ 
DELIMITER ; 



