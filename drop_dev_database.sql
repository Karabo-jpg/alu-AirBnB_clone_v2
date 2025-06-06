-- Drop and recreate the development database
DROP DATABASE IF EXISTS hbnb_dev_db;
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
USE hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES; 