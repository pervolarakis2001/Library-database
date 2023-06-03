
-- 3.1.1 
select sch.name as school, count(borrowed_id) as count from borrowings bor 
                        INNER JOIN operator op ON bor.operator_id = op.operator_id 
                        INNER JOIN school sch ON  sch.operator_id = op.operator_id WHERE MONTH(borrowing_date) ='{month}' AND YEAR(borrowing_date) ='{year}'
                        GROUP BY sch.name;

select distinct * from books b inner join category_table ct on b.ISBN = ct.ISBN;
select * from books;

-- 3.1.2
SELECT  category, us.First_name, us.Last_name FROM books b 
                        INNER JOIN category_table ct ON b.ISBN = ct.ISBN
                        INNER JOIN borrowings bor ON bor.ISBN = ct.ISBN
                        INNER JOIN school_users schu ON bor.school_users_id = schu.school_users_id
                        INNER JOIN users us ON us.user_id = schu.school_users_id
                        WHERE schu.status = "teacher" AND borrowing_date > DATE_ADD(curdate(),interval -1 year) 
                         AND category='{category}' ;   

SELECT ct.category, author FROM books b 
                        INNER JOIN category_table ct ON b.ISBN = ct.ISBN
                        LEFT JOIN author_table aut ON ct.ISBN = aut.ISBN
                        WHERE category='{category}' ; 

-- 3.1.3 


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

-- 3.1.4
select distinct aut.author from author_table aut
                    LEFT JOIN borrowings bor ON bor.ISBN = aut.ISBN
                    WHERE not exists (select 1 from borrowings inner join author_table aut1 on bor.ISBN = aut1.ISBN );
-- 3.1.5

select bor.operator_id, us.First_name, us.Last_name,count(bor.borrowed_id) as count from users us
                    inner join operator op on op.operator_id = us.user_id
                    inner join borrowings bor on bor.operator_id = op.operator_id  
                    inner join operator op1 on op1.operator_id = op.operator_id WHERE YEAR(bor.borrowing_date) IN (
                        SELECT DISTINCT YEAR(borrowing_date)
                        FROM borrowings
                    )
                    group by  bor.operator_id, us.First_name, us.Last_name
                    having count(bor.borrowed_id) > 20 ; 
		    
-- 3.1.6 
select ct1.category as cat1, ct2.category as cat2, count(bor.borrowed_id) as count from borrowings bor 
                    inner join books b on b.ISBN = bor.ISBN 
                    inner join category_table ct1 on ct1.ISBN = b.ISBN 
                    cross join category_table ct2 on ct1.category <> ct2.category  AND ct1.category < ct2.category AND ct1.ISBN = ct2.ISBN
                    group by ct1.category,ct2.category
                    ORDER BY
                    COUNT(bor.borrowed_id) DESC
                    limit 3;


-- 3.1.7

    
with aut_five_less_max (author,count_of_books_per_author) as
		(select aut.author, count(b.ISBN) as count_of_books_per_author from books b 
		inner join author_table aut on aut.ISBN = b.ISBN 
		group by aut.author),
	 most_books_author (max_books_author) as
		(select max(count_of_books_per_author) as max_books_author 
        from aut_five_less_max)
select aflm.author, aflm.count_of_books_per_author
from aut_five_less_max aflm
join most_books_author mba 
on mba.max_books_author - 5 > aflm.count_of_books_per_author;

-- 3.2.1
SELECT b.isbn,b.title,b.publisher, b.num_of_pages, b.avail_copies, b.language, a.author, c.category FROM books b  inner join author_table a on a.ISBN = b.ISBN inner join school sch on sch.school_id = b.school_id 
            inner join category_table c on c.ISBN= b.ISBN 
            WHERE title ='{title}' AND category='{category}' AND author='{author}' AND avail_copies = {avail_copies} AND b.operator_id ={session.get('user_id')}

-- 3.2.2 
select * from borrowings;
select bor.school_users_id, us.First_name, us.Last_name from users us
inner join borrowings bor on bor.school_users_id = us.user_id
where due_date < curdate() and return_date is null
having count(bor.borrowed_id) > 1;


select avg(rating_score) as score,school_users_id,category from ratings r INNER JOIN category_table c  on c.Isbn = r.ISBN WHERE 
             r.school_users_id = {sch_user_id} and c.category = '{category}'

-- 3.3.1

-- 3.3.2
select bor.school_users_id, us.First_name, us.Last_name, b.ISBN, b.title from borrowings bor 
inner join books b on b.ISBN = bor.ISBN
inner join users us on us.user_id = bor.school_users_id
group by bor.school_users_id; 
-- vasi toy parapanw tha psaxnei kai kala o mathitis stin kartela mesw tou student id tou h tou onomatepwnymou tou
