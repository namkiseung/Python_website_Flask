CREATE TABLE notice_board (idx integer PRIMARY KEY AUTOINCREMENT, 
    id varchar(20) NOT NULL, 
    title varchar(50) NOT NULL, 
    content varchar(250) NOT NULL, 
    day varchar(30) NOT NULL, 
    files varchar(200),
    countview integer DEFAULT 0
); 
