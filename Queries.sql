use library; 

-- 3.1.1 
select * from borrowings;
select sch.name, count(borrowed_id) from borrowings bor 
INNER JOIN operator op ON bor.operator_id = op.operator_id 
INNER JOIN school sch ON  sch.operator_id = op.operator_id 
GROUP BY sch.name;
-- leipoun kritiria anazitisis

select distinct * from books b inner join category_table ct on b.ISBN = ct.ISBN;
select * from books;

-- 3.1.2
SELECT ct.category, aut.author FROM books b 
INNER JOIN category_table ct ON b.ISBN = ct.ISBN
LEFT JOIN author_table aut ON ct.ISBN = aut.ISBN
GROUP BY aut.author ORDER BY ct.category;

SELECT ct.category, schu.school_users_id, us.First_name, us.Last_name FROM books b 
INNER JOIN category_table ct ON b.ISBN = ct.ISBN
INNER JOIN borrowings bor ON bor.ISBN = ct.ISBN
INNER JOIN school_users schu ON bor.school_users_id = schu.school_users_id
INNER JOIN users us ON us.user_id = schu.school_users_id
WHERE schu.status = "teacher" AND borrowing_date > DATE_ADD(curdate(),interval -1 year) ORDER BY ct.category ASC;


-- 3.1.3 
--select schu.school_users_id, us.First_name, us.Last_name, count(bor.borrowed_id) from books b
--INNER JOIN  borrowings bor ON bor.ISBN = b.ISBN
--INNER JOIN school_users schu ON bor.school_users_id = schu.school_users_id
--INNER JOIN users us ON us.user_id = schu.school_users_id
--WHERE year(CURDATE()) - DATE_FORMAT(schu.age,"%Y")  < 40 AND schu.status = "teacher";
-- exun daneistei ta perissotera vivlia, idk ti ennoei me ayto 

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
SELECT DISTINCT aut.author FROM author_table aut
LEFT JOIN borrowings bor ON bor.ISBN = aut.ISBN
WHERE bor.borrowed_id is NULL;
-- mporei na lythei kai me subquery tha to dw argotera an ayti h lysi einai lathos
-- me subquery
select distinct aut.author from author_table aut
LEFT JOIN borrowings bor ON bor.ISBN = aut.ISBN
WHERE not exists (select 1 from borrowings inner join author_table aut1 on bor.ISBN = aut1.ISBN );

-- 3.1.5
select op.operator_id, us.First_name, us.Last_name,count(bor.borrowed_id) from users us
inner join operator op on op.operator_id = us.user_id
inner join borrowings bor on bor.operator_id = op.operator_id  
inner join operator op1 on op1.operator_id = op.operator_id 
group by bor.operator_id 
having count(bor.borrowed_id) > 20; 
-- havent put 1 year interval and probably the equality of operator borrowings  

-- 3.1.6 
-- 2OO books 100 of them have 2 categories
SELECT cat.category, cat.ISBN FROM category_table cat INNER JOIN borrowings bor ON bor.ISBN = cat.ISBN   WHERE cat.ISBN in(
SELECT ISBN FROM category_table 
group by ISBN having count(cat.category)>1);

select ct1.category, ct2.category, count(bor.borrowed_id) from borrowings bor 
inner join books b on b.ISBN = bor.ISBN 
inner join category_table ct1 on ct1.ISBN = b.ISBN 
cross join category_table ct2 on ct1.category <> ct2.category  AND ct1.category < ct2.category AND ct1.ISBN = ct2.ISBN
group by ct1.category,ct2.category
limit 3;

 select distinct ct1.category,ct2.category from category_table ct1 cross join category_table ct2 
 on ct1.category <> ct2.category  AND ct1.category < ct2.category;


-- 3.1.7
-- select all the authors with their respectable amount of books 
select aut.author, count(b.ISBN) as count_of_books_per_author from books b 
	inner join author_table aut on aut.ISBN = b.ISBN 
    group by aut.author;
    
-- select author with maximum books 
select z.author, max(z.count_of_books_per_author) as max_books_author from 
    (select aut.author, count(b.ISBN) as count_of_books_per_author from books b 
	inner join author_table aut on aut.ISBN = b.ISBN 
	group by aut.author) z;
    
-- answer the question
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

-- 3.2.1
select title,author from books inner join author_table on books.ISBN = author_table.ISBN;

-- 3.2.2 
select * from borrowings;
select bor.school_users_id, us.First_name, us.Last_name from users us
inner join borrowings bor on bor.school_users_id = us.user_id
where due_date < curdate() and return_date is null
having count(bor.borrowed_id) > 1;
-- thelei diorthwsi, einai lathos 

-- 3.2.3

--select school_users_id, avg(z.num_of_ratings_per_borrower) as avg_num_of_ratings_per_borrower from 
	--(select school_users_id, count(rating_id) as num_of_ratings_per_borrower from ratings group by school_users_id) z
   -- group by school_users_id;


--select category, avg(z.num_of_ratings_per_category) as avg_num_of_ratings_per_category from 
--	(select cat.category, count(r.rating_id) as num_of_ratings_per_category from ratings r inner join category_table cat on cat.ISBN = r.ISBN
  --  group by cat.category) z
 --   group by category;

select avg(rating_score) as score,school_users_id,category from ratings r INNER JOIN category_table c  on c.Isbn = r.ISBN WHERE 
             r.school_users_id = {sch_user_id} and c.category = '{category}'

-- 3.3.1
select * from reservations;
select * from borrowings;
-- 3.3.2
select bor.school_users_id, us.First_name, us.Last_name, b.ISBN, b.title from borrowings bor 
inner join books b on b.ISBN = bor.ISBN
inner join users us on us.user_id = bor.school_users_id
group by bor.school_users_id; 
-- vasi toy parapanw tha psaxnei kai kala o mathitis stin kartela mesw tou student id tou h tou onomatepwnymou tou
