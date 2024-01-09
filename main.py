import sqlite3

con = sqlite3.connect("library.sqlite")
f_damp = open('library.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()

con.executescript(damp)
con.commit()
cursor = con.cursor()

cursor.execute("SELECT * FROM author")
print(cursor.fetchall())
cursor.execute("SELECT * FROM reader")
print(cursor.fetchall())


#ЗАДАНИЕ1

first_task_query = """
  SELECT
    b.title AS title,
    r.reader_name AS reader,
    (julianday(br.return_date) - julianday(br.borrow_date) + 1) AS days
  FROM
    book_reader br
  JOIN
    book b ON br.book_id = b.book_id
  JOIN
    reader r ON br.reader_id = r.reader_id
  WHERE
    br.return_date IS NOT NULL
    AND (julianday(br.return_date) - julianday(br.borrow_date) + 1) > 14
  ORDER BY
    title ASC,
    days DESC,
    r.reader_name ASC;
"""
cursor.execute(first_task_query)
results = cursor.fetchall()
for row in results:
  print(row)

#ЗАДАНИЕ2
  
secont_task_query = """
  SELECT
    b.title AS Название,
    p.publisher_name AS Издательство,
    b.year_publication AS Год,
    COUNT(br.book_id) AS Количество
  FROM
    book_reader br
  JOIN
    book b ON br.book_id = b.book_id
  JOIN
    publisher p ON b.publisher_id = p.publisher_id
  GROUP BY
    br.book_id
  ORDER BY
    Название ASC,
    Издательство ASC,
    Год DESC,
    Количество DESC
  LIMIT 1;
"""

cursor.execute(first_task_query)
results = cursor.fetchall()
for row in results:
  print(row)


#ЗАДАНИЕ3

# Создание таблицы new_book и заполнение ее данными
  
create_new_book = """
  CREATE TABLE IF NOT EXISTS new_book (
    title VARCHAR(80),
    publisher_name VARCHAR(80),
    year_publication INT,
    amount INT
  );
"""

new_book_init = """
  INSERT INTO new_book(title, publisher_name, year_publication, amount)
  VALUES
  ("Вокруг света за 80 дней", "ДРОФА", 2019, 2),
  ("Собачье сердце", "АСТ", 2020, 3),
  ("Таинственный остров", "РОСМЭН", 2015, 1),
  ("Евгений Онегин", "АЛЬФА-КНИГА", 2020, 4),
  ("Герой нашего времени", "АСТ", 2017, 1);
"""

update_book = """
  UPDATE book
    SET available_numbers = available_numbers + nb.amount
    FROM new_book nb
    WHERE
      book.title = nb.title
      AND book.publisher_id = (SELECT publisher_id FROM publisher WHERE publisher_name = nb.publisher_name)
      AND book.year_publication = nb.year_publication;
"""

# Добавление информации о новых книгах
add_new_book = """
INSERT INTO book (title, genre_id, publisher_id, year_publication, available_numbers)
  SELECT
    nb.title,
    NULL, -- NULL для жанра, так как вы сказали его оставить пустым
    (SELECT publisher_id FROM publisher WHERE publisher_name = nb.publisher_name),
    nb.year_publication,
    nb.amount
  FROM new_book nb
  WHERE NOT EXISTS (
    SELECT 1
    FROM book b
    WHERE
      b.title = nb.title
      AND b.publisher_id = (SELECT publisher_id FROM publisher WHERE publisher_name = nb.publisher_name)
      AND b.year_publication = nb.year_publication
);
"""

cursor.execute(create_new_book)
cursor.execute(new_book_init)
cursor.execute(update_book)
cursor.execute(add_new_book)
con.commit()



#ЗАДАНИЕ 5

window_function = """
  SELECT
    b.title AS Название,
    g.genre_name AS Жанр,
    p.publisher_name AS Издательство,
    CASE
        WHEN b.available_numbers > ROUND(AVG(b.available_numbers) OVER (), 0) THEN 'больше на '
        WHEN b.available_numbers < ROUND(AVG(b.available_numbers) OVER (), 0) THEN 'меньше на '
        ELSE 'равно среднему'
    END || ABS(b.available_numbers - ROUND(AVG(b.available_numbers) OVER (), 0)) AS Отклонение
  FROM
    book b
  JOIN
    genre g ON b.genre_id = g.genre_id
  JOIN
    publisher p ON b.publisher_id = p.publisher_id
  ORDER BY
    Название ASC,
    Отклонение ASC;
"""

cursor.execute(window_function)
con.close()