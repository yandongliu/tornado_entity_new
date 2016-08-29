# Tornado Boilerplate Application

# Overview
Model-View-Controller-Service architecture

# Handlers
- Async HTTP Client: http://localhost:8888/async_fetch?url=http://www.cnn.com

# Set up
- fab bootstrap_database
- fab create_tables
- fab fake_item

# one of following sets the password
- CREATE USER 'tornado_user'@'localhost' IDENTIFIED BY 'qwerty123!';
- set password for tornado_user@localhost = password('qwerty123!');
- GRANT ALL PRIVILEGES ON tornado_app.* TO 'tornado_user'@'localhost';
