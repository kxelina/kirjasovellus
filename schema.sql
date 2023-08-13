CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);


CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE, 
    user_icon BYTEA,
    file_extension TEXT
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    publication_year INTEGER,
    description_text TEXT,
    genre TEXT,
    reading_time INTEGER
);

CREATE TABLE folders (
    folder_id SERIAL PRIMARY KEY,
    folder_name TEXT,
    username TEXT 
);

CREATE TABLE books_in_folder (
    bookfolder_id SERIAL PRIMARY KEY,
    folder_id INTEGER,
    book_id INTEGER, 
    username TEXT 
);

CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name TEXT
);

CREATE TABLE book_genre (
    book_id INTEGER,
    genre_id INTEGER
);

CREATE TABLE review (
    review_id SERIAL PRIMARY KEY,
    book_id INTEGER,
    username TEXT, 
    review_text TEXT, 
    rating INTEGER
);