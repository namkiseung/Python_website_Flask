CREATE TABLE notice_board (idx integer PRIMARY KEY AUTOINCREMENT, 
    id varchar(20), 
    title varchar(50), 
    content varchar(250), 
    day varchar(30), 
    files varchar(200),
    countview integer DEFAULT 0
); 
