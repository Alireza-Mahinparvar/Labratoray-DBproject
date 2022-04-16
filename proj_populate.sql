use Laboratory;
insert department values
('1','Oncology'),
('2','Cardiology'),
('3','Neurology');

insert employee values
( 'e1', 'Jessica', 'Seto', 2, 'PhD Neurobiology',1,0,0, '$2b$12$07CcdYXd9szSi2zdCyX5OeyzH2L7WOLUwMAHQc5Y7TLmO//zfao5S', NULL,  '3'),
( 'e2', 'Andrew', 'Wickham', 1, 'PhD Radiation Oncology',0,1,0, '$2b$12$3vMY8nqHbu0BpbY/XTuwt.XY2I9.hA7uFdKAiyXnhDx.VSNPHySU6', NULL,  '1'),
( 'e3', 'Alexander', 'Robin', 2, 'PhD Tumor Immunology',1,0,0, '$2b$12$XBLFrP7mxoVyCBhiuvtZZeO5bzph5s82fELIRiwGxa.lsOepsw.LG', NULL,  '1'),
( 'e4', 'Tony', 'Clewans', 1, 'BS Chemistry',0,0,1, '$2b$12$osBiHc8tXSWE78txaIuEZekXP6dSTr/inTfzykTf41EBJGFHE80au', NULL,  '3'),
( 'e5', 'John', 'Miller', 3, 'PhD Neurology',0,1,0, '$2b$12$/4rBbhKJ1P95Ixb2GHqPvOxT63ymjiMb0TelYm0EnGNd3.GkqM2mq', NULL,  '3'),
( 'e6', 'Cole', 'Smith', 3, 'PhD Cardiology',1,0,0, '$2b$12$Ki8adsKK1/XeViHl35gg7uaGgZDc2FdO2N0GW80kYR2rI9gerFdKC',  NULL, '2'),
( 'e7', 'Chloe', 'Miller', 2, 'PhD Cardiology',0,1,0, '$2b$12$rIAn1RzAZ/iTY1WlYF2VIeETWLHiR4owEVYS9GW.IWY5Qf87IKcZq', NULL,  '2'),
( 'e8', 'Chris', 'Johnson', 1, 'MS Biology',0,0,1, '$2b$12$GIOFM.1Es41xiYydogdI4OI16i2hkRkwZtMjLxBsm3C20xjcFSvOe', NULL,  '2'),
( 'e9', 'chris', 'Ben ', 1, 'MS chemistry',0,0,1, '$2b$12$3ncSDcMnYC.1EeAjGPhyK.sPZg1D5ZCEMFrPf5p5067Beocoblmh6', NULL,  '1'),
( 'e10', 'Rahman ', 'Aziz', 2, 'PhD Neurobiology',1,0,0, '$2b$12$wsG93w.gdPoa7.CE0dz9DezP4bVptngaTJ1crl9Yf8VFYRBQ.onmu', NULL,  '3'),
( 'e11', 'Nikki', 'Glaser', 1, 'MS Biology',0,0,1, '$2b$12$wncjhbL7KHfIpcx4J68ZhOTxOVf0WeB9VX4Af2DedpAcH0GST6RRu', NULL,  '2'),
( 'e12', 'Emily', 'Jordan ', 1, 'MS Biology',0,0,1, '$2b$12$6TyEVA6eOIJSDoD/jzppReE.4z1ARo0tx5INp2ovHJQqLEkO1Cw3G', NULL,  '1'),
( 'e13', 'Ivanka', 'Addams', 2, 'PhD Neurobiology',1,0,0, '$2b$12$xMTWY/2i..EUny8RcxbNruDzTYz8mkegPuYZDaUKL/x0hCNegVhiu', NULL,  '3'),
( 'e14', 'Julie', 'Geller', 1, 'PhD Tumor Immunology',0,0,1, '$2b$12$hqm9PT7.as4VUGc7qCi4TuFE/sP7sbTMGtkH62TjlcLh9X7dq56Nm', NULL,  '2'),
( 'e15', 'Alexander ', 'MacQueen', 2, 'PhD Tumor Immunology',1,0,0, '$2b$12$UnU5nGKvTmSzmGGue2O25O132z4FertNHcviZcZzisqMatCxflZTS', NULL,  '1'),
( 'e16', 'Christian', 'Ruzich', 1, 'PhD Radiation Oncology',0,0,1, '$2b$12$MKzHrndtDYDWLFqcNy6aLedRMKXpOx.q1n8mOOwrxKW7CGwBBAbze', NULL,  '1'),
( 'e17', 'Andy', 'Korby', 1, 'BS Chemistry',0,0,1, '$2b$12$Szd2IAZQFFbgdxHCNzhtiey.Ih2TWKO3SsfLw.IRWDD/woIDHTK0a', NULL,  '3'),
( 'e18', 'Joe', 'William', 1, 'PhD Radiation Oncology',0,0,1, '$2b$12$CJ8vXrAhAX0XIUvnBeNyHebpi1Kgv8f0zHWuczXY2nbtN5wfg6gsS', NULL,  '1'),
( 'e19', 'Christian', 'Bale', 1, 'MS Biology',0,0,1, '$2b$12$u5AfSI5D8weTbP/NmvJkLeeocBvjaCABUJdAMO3vFYjuyRR.RESKy', NULL,  '2'),
( 'e20', 'Charlie', 'Brown', 1, 'BS Biology',0,0,1, '$2b$12$Bm6TbfJQmvW4GouuFOa1GuDgBClrRJy/r4BPs0wIAUJ.tF1npeq2.', NULL,  '2');
update employee set supervisor_id = 'e7' where emp_id = 'e6'; -- adding supervisor here since their supervisor gets made after them

-- Adding this line to make current proj_init to work
ALTER TABLE department ADD column dept_head varchar(5);
ALTER TABLE department ADD column start_date date;
update department set dept_head = 'e7', start_date = '2020-01-02' where dept_id = '2';
update department set dept_head = 'e2', start_date = '2019-10-05' where dept_id = '1';
update department set dept_head = 'e5', start_date = '2020-07-21' where dept_id = '3';
-- Might need to create a new relationship table just to prevent circular reference between dep and emp
-- Otherwise we can't add new department if foreign key is non nullable
ALTER TABLE department add constraint FOREIGN KEY  (dept_head) references employee(emp_id);

insert project values
('5','Exercise and Cardiac Output','2020-03-07','2021-07-01','done','2','e7'),
('6','Energy Drink and the Heart','2020-03-07','2021-07-01','ongoing','2','e7');

-- experiment missing description column
insert experiment values
('5','Heart rate survey','2020-07-05','2020-12-11','Done','5','e7','2020-05-01',0),
('6','One year study on energy drink','2020-07-05',NULL,'Ongoing','6','e7','2020-05-06',1);

insert trial values
('6','Some Criteria',20,60,'A',10);




insert  publication values
('3','Effects of Exercise on Cardiac Output','American Heart Association',
NULL,'e7','2021-01-15');

insert test_subject values
( 'ts1', 'M', '1992-06-14', 'reg', 'anastacio', '$2b$12$3sxNz0q429ySLeUw4M/VbOceOvXWQ0DnC8dk02eru5wU9lrc9NSlO'),
( 'ts2', 'M', '1976-04-03', 'umang', 'dalsania', '$2b$12$/0swWLO4SSyrUK0CJ0CkSOdJTLy0gMnFJ6vHO/0hD9VxOmTqJ3Dx6'),
( 'ts3', 'M', '1966-07-07', 'adam', 'goldstein', '$2b$12$FD7TTtuHXu0WnKQoLH9ew.2ECJ.ui/Piur5Z4nXknDvQaSagO7uKC'),
( 'ts4', 'F', '1940-07-19', 'megha', 'jain', '$2b$12$IczQ0TdJfLwTPT/WPBF8Aueef4tc3GIQgzR.LgCoqCk.uKRikxgR.'),
( 'ts5', 'M', '1960-04-18', 'alireza', 'parvar', '$2b$12$764UFYDDd5CORObrzbJMQeGIVtVnCnzx8S6PMLtOeMKfYPKHt5DnS'),
( 'ts6', 'M', '1975-08-23', 'khoa', 'nyugen', '$2b$12$yfVlFmHCYMp1yHHjtXhrxOzbOec.JRDDKdc03FTPXLIvxl0NX/C1a'),
( 'ts7', 'M', '1998-10-02', 'john', 'Johnson', '$2b$12$C/KSPsFiIo8cPQqeabmvj.0//bcmXBzu3avHHmeuYbcOmrvN8vO9e'),
( 'ts8', 'F', '1991-12-05', 'Gini', 'Belowski', '$2b$12$22PZNLLQB7FEtSWEESp/fOjRDCEfvmPYP.zSWbwBszX90ozgNuIMq'),
( 'ts9', 'F', '1981-11-05', 'Monica', 'Smoth', '$2b$12$qbDTQml7/r/3yAWzeCmpGe41Idmxs8qE4GGzc6N2OwQ1vz7R1wU7y'),
( 'ts10', 'F', '1981-11-04', 'antonie ', 'robins', '$2b$12$g9zLOgWO9zRixm9ZOuRYcupNEW4yBfBxJ2I1CLcoiTWgIvhaFWRUO'),
( 'ts11', 'M', '2001-10-01', 'james', 'baylor', '$2b$12$2hh36yI0vij4rzM213qroePgBYu6uHByoGMEBB2eAiOd35.2N11Om'),
( 'ts12', 'M', '1940-08-17', 'henry', 'fisher', '$2b$12$5kjvs9bgBG/RBkBYXyiG.OcuZ4j5s6xlUaE57Vsh1VjuMUXR8orhm');

insert equipment values
( '1', 'Holter Monitor', 'e8'),
( '2', 'Treadmill', 'e20'),
( '3', 'Funnels', NULL),
( '4', 'Burets', NULL),
( '5', 'watch glasses', NULL),
( '6', 'flasks', NULL),
( '7', 'cylinder', NULL),
( '8', 'beaker', NULL),
( '9', 'thermometer', NULL),
( '10', 'balances', NULL),
( '11', 'googles', NULL),
( '12', 'pcr', NULL),
( '13', 'centrifuge', NULL),
( '14', 'vortexer', NULL),
( '15', 'fume hood', NULL),
( '16', 'pipet', NULL),
( '17', 'Pet Scanner', NULL),
( '18', 'CT Scanner', NULL),
( '19', 'MRI Machine', NULL),
( '20', 'Treadmill', NULL);

insert works_on values
('e6','5');

insert drafts values
('e6','3');

insert conducts_experiments values
('e6','5'),
('e7','6');


insert participates values
('ts1','6'),
('ts2','6'),
('ts4','6');

insert assigned_to values
('1','5','2020-11-02','2020-12-05','e20'),
('2','5','2020-11-12','2020-12-15','e8'),
('4','5','2020-11-10',NULL,'e9'),
('3','5','2020-11-10',NULL,NULL);

insert conducts_trials values 
('e6','6');

insert administrator values 
('a1','$2b$12$WgXOUhc9oYRSAy9F66RXC.uxtiTCq//h17FyAyuBbOCBbSb2EAROa');

