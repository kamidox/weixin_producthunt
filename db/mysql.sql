# mysql -uroot -pkamidox -Dproducthunt < /path/to/mysql.sql
USE producthunt;
# products table
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  description TEXT,
  url TEXT,
  postid TEXT,
  comment_url TEXT,
  postdate TEXT,
  vote_count INT,
  comment_count INT,
  updated DATETIME,
  userid TEXT
) DEFAULT CHARSET=utf8;

# user table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER auto_increment PRIMARY KEY,
  userid TEXT,
  name TEXT,
  icon TEXT,
  title TEXT
) DEFAULT CHARSET=utf8;

# comment table
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  id INTEGER auto_increment PRIMARY KEY,
  commentid TEXT,
  parentid TEXT,
  postid TEXT,
  userid TEXT,
  vote_count INT,
  is_child BOOLEAN,
  comment_html TEXT,
  comment TEXT
) DEFAULT CHARSET=utf8;
