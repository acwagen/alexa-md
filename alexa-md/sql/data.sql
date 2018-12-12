INSERT INTO Patients(P_First,P_Last) VALUES
("alyssa","w"),
("anthony", "s"),
("derek", "y"),
("mike", "w");

INSERT INTO Collections(C_Name,PID, Study) VALUES
("alyssa_CT",1,"CT"),
("alyssa_MR",1,"MR"),
("anthony_CT",2,"CT"),
("anthony_MR",2,"MR"),
("derek_CT",3,"CT"),
("derek_MR",3,"MR"),
("mike_CT",4,"CT"),
("mike_MR",4,"MR");

INSERT INTO Images(IID,CID,IND) VALUES
("alyssa1.jpeg",1,0),
("alyssa2.jpeg",2,0),
("anthony1.jpeg",3,0),
("anthony2.jpeg",4,0),
("derek1.jpeg",5,0),
("derek2.jpeg",6,0),
("mike1.jpg",7,0),
("mike2.jpg",8,0),
("alyssa3.jpg",1,1);
