
use sql_intro;

CREATE TABLE user(
	user_id int auto_increment not null,
   name VARCHAR(50),
   email varchar(50),
   password varchar(50),
   CONSTRAINT UC_User UNIQUE (email),
   PRIMARY KEY (user_id)
);
create table Note(
note_id int auto_increment not null,
content text,
category varchar(50),
primary key (note_id)
);
create table user_note(
user_id int,
   note_id int,
   FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY(note_id) REFERENCES Note(note_id),
	primary key(user_id, note_id)
    );

