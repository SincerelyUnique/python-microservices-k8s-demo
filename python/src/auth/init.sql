create user 'auth_user'@'localhost' identified by 'Aauth123';

create database auth;

grant all privileges on auth.* to 'auth_user'@'localhost';

use auth;

create table user(
    id int not null  auto_increment primary key ,
    email varchar(255) unique not null ,
    password varchar(255) not null
);

insert into user(email, password) values ('georgio@email.com', 'Admin123');
