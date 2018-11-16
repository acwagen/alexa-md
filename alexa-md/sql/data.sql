INSERT INTO Patients(P_First,P_Last) VALUES
("alyssa","w"),
("anthony", "s"),
("derek", "y"),
("mike", "w");

INSERT INTO Collections(C_Name,PID, Study) VALUES
("allysa_CT",1,"CT"),
("allysa_MRI",1,"MRI"),
("anthony_CT",2,"CT"),
("anthony_MRI",2,"MRI"),
("derek_CT",3,"CT"),
("derek_MRI",3,"MRI"),
("mike_CT",4,"CT"),
("mike_MRI",4,"MRI");

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
