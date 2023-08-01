CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);


CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    user_icon BYTEA
);

-- CREATE TABLE books (
--     book_id SERIAL PRIMARY KEY,
--     title TEXT,
--     author TEXT,
--     publication_year INTEGER,
--     description TEXT,
--     category TEXT,
--     reading_time INTEGER,
--     user_id INTEGER,
--     FOREIGN KEY (user_id) REFERENCES users (user_id)
-- );

CREATE TABLE folders (
    folder_id SERIAL PRIMARY KEY,
    name TEXT,
    username TEXT
);

-- CREATE TABLE genre (
--     genre_id SERIAL PRIMARY KEY,
--     name TEXT
-- );

-- CREATE TABLE book_genre (
--     book_id INTEGER,
--     genre_id INTEGER,
--     PRIMARY KEY (book_id, genre_id),
--     FOREIGN KEY (book_id) REFERENCES books (book_id),
--     FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
-- );

-- CREATE TABLE feedback (
--     feedback_id SERIAL PRIMARY KEY,
--     book_id INTEGER,
--     user_id INTEGER,
--     text TEXT NOT NULL,
--     FOREIGN KEY (book_id) REFERENCES books (book_id),
--     FOREIGN KEY (user_id) REFERENCES users (user_id)
-- );