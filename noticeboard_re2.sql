CREATE TABLE notice_board_re2 (idx integer PRIMARY KEY AUTOINCREMENT,
    originidx integer,
    origin_reidx integer, 
    id varchar(20) NOT NULL,  
    content varchar(250), 
    day varchar(30)
); 
