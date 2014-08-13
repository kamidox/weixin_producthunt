# mysql -uroot -pkamidox -Dproducthunt < /path/to/mysql.sql
USE producthunt;
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  description TEXT,
  url TEXT,
  comment_url TEXT,
  postdate TEXT,
  vote_count INT,
  user_name TEXT,
  login_name TEXT,
  user_icon TEXT,
  user_title TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;
