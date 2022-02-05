CREATE TABLE notice_board_re (idx integer PRIMARY KEY AUTOINCREMENT,
    originidx integer, 
    id varchar(20) NOT NULL,  
    content varchar(250) NOT NULL, 
    day varchar(30) NOT NULL
); 
