-- SJSU CMPE 138 Fall 2021 TEAM12
drop database if exists Laboratory;
create database Laboratory;
use Laboratory;

create table department
(    
    dept_id         varchar(5) not null,
    dept_name       varchar(30) not null, 
    primary key (dept_id)
);

create table employee
(    
    emp_id             varchar(5),
    emp_fname        varchar(25), 
    emp_lname        varchar(25),
    security_level    int,
    credential        varchar(25),
    rs_flag            tinyint(1),
    pi_flag            tinyint(1),
    la_flag            tinyint(1),
    hashed_pass        varchar(60),
    supervisor_id    varchar(5),
    dept_id            varchar(5),
    constraint sec_level_check check (security_level > 0 and security_level < 4),
    primary key (emp_id),
    foreign key (dept_id) references department(dept_id)
        on delete cascade
        on update cascade,
    foreign key (supervisor_id) references employee(emp_id)
        on delete set null
);

create table project
(    
    pro_id             varchar(5),
    pro_name        varchar(50), 
    pro_sdate        date,
    pro_edate        date,
    pro_status        varchar(10),
    dept_id				varchar(5),
    proj_leader			varchar(5),
    constraint status_check_pro check (pro_status = 'ongoing' or pro_status = 'done' or pro_status = 'planned'),
    primary key (pro_id),
    foreign key (dept_id) references department(dept_id)
		on delete cascade
        on update cascade,
    foreign key (proj_leader) references employee(emp_id)
		on delete set null
        on update cascade
);

create table experiment
(
    exp_id          varchar(5) not null,
    exp_name        varchar(50) not null, 
    exp_sdate       date,
    exp_edate       date,
    exp_status      varchar(10) not null,
    pro_id          varchar(5)  not null,
    approved_by     varchar(5),
    approved_date   date,
	trial_flag      tinyint(1) not null,
    constraint status_check_exp check (exp_status = 'ongoing' or exp_status = 'done' or exp_status = 'planned'),
    primary key (exp_id),
    foreign key (pro_id) references project(pro_id)
		on delete cascade
        on update cascade,
    foreign key (approved_by) references employee(emp_id)
		on delete set null
        on update cascade
);

create table trial
(    
    exp_id          varchar(5),  
    criteria        varchar(50),
    agerange_start  int check (agerange_start >= 18),
    agerange_end    int check (agerange_end <= 80),
    gender          varchar(1),
    num_allowed_participants int check (num_allowed_participants > 0),
	constraint gender_check check (gender='M' or gender='F' or gender='A'),
    primary key (exp_id),
    foreign key (exp_id) references experiment(exp_id)
		on delete cascade
        on update cascade
);



-- old trial
-- create table trial
-- (    
--     exp_id            varchar(5),
--     exp_name        varchar(50), 
--     exp_sdate        date,
--     exp_edate        date,
--     exp_status        varchar(10),
--     criteria        varchar(50),
--     agerange_start    int check (agerange_start >= 18),
--     agerange_end    int check (agerange_end <= 80),
--     gender            varchar(1),
--     num_allowed_participants int check (num_allowed_participants > 0),
--     pro_id            varchar(5),
-- 	constraint gender_check check (gender='M' or gender='F' or gender='A'),
--     constraint status_check_trial check (exp_status = 'ongoing' or exp_status = 'done' or exp_status = 'planned'),
--     primary key (exp_id),
--     foreign key (pro_id) references project(pro_id)
-- );

create table publication
(    
    pub_id          varchar(5) not null,
    pub_name        varchar(50) not null,
    pub_status      varchar(10) not null,
    journal         varchar(30) not null,
    date_published  date,
    approved_by     varchar(5),
    approved_date   date,
    pro_id          varchar(5),
    constraint status_check_pub check (pub_status = 'ongoing' or pub_status = 'done' or pub_status = 'planned'),
    foreign key (approved_by) references employee(emp_id)
		on delete set null
        on update cascade,
    foreign key (pro_id) references project(pro_id)
		on delete cascade
        on update cascade,
    primary key (pub_id)
);

create table test_subject
(    
    ts_id           varchar(5),
    gender          varchar(1),
    ts_dob          date,
    ts_fname        varchar(20),
    ts_lname        varchar(20),
    hashed_pass     varchar(60),
    constraint gender_check_ts check (gender = 'M' or gender = 'F'),
    primary key (ts_id)
);

create table equipment
(    
    equ_id          varchar(5),
    equ_name        varchar(50),
    maintained_by	varchar(5),
    primary key (equ_id),
    foreign key (maintained_by) references employee(emp_id)
		on delete set null
        on update cascade
);

create table works_on
(    
    emp_id            varchar(5),
    pro_id            varchar(5),
    primary key (emp_id, pro_id),
    foreign key (emp_id) references employee(emp_id)
        on delete cascade
        on update cascade,
    foreign key (pro_id) references project(pro_id)
        on delete cascade
        on update cascade
);

create table drafts
(    
    emp_id            varchar(5),
    pub_id            varchar(5),
    primary key (emp_id, pub_id),
    foreign key (emp_id) references employee(emp_id)
		on update cascade
        on delete cascade,
    foreign key (pub_id) references publication(pub_id)
		on update cascade
        on delete cascade
);

create table conducts_experiments
(    
    emp_id            varchar(5),
    exp_id            varchar(5),
    primary key (emp_id, exp_id),
    foreign key (emp_id) references employee(emp_id)
		on update cascade
        on delete cascade,
    foreign key (exp_id) references experiment(exp_id)
		on update cascade
        on delete cascade
);

create table conducts_trials
(    
    emp_id            varchar(5),
    exp_id            varchar(5),
    primary key (emp_id, exp_id),
    foreign key (emp_id) references employee(emp_id)
		on update cascade
        on delete cascade,
    foreign key (exp_id) references trial(exp_id)
		on update cascade
        on delete cascade
);

create table participates
(    
    ts_id            varchar(5),
    exp_id            varchar(5),
    primary key (ts_id, exp_id),
    foreign key (ts_id) references test_subject(ts_id)
		on update cascade
        on delete cascade,
    foreign key (exp_id) references trial(exp_id)
		on update cascade
        on delete cascade
);

create table assigned_to
(    
    equ_id            varchar(5),
    exp_id            varchar(5),
    exp_sdate        date,
    exp_edate        date,
    monitor_id        varchar(5),
    primary key (equ_id, exp_id),
    foreign key (equ_id) references equipment(equ_id)
		on update cascade
        on delete cascade,
    foreign key (exp_id) references experiment(exp_id)
		on update cascade
        on delete cascade,
    foreign key (monitor_id) references employee(emp_id)
		on update cascade
        on delete set null
);

create table administrator
(
    emp_id          varchar(5),
    hashed_pass        varchar(60),
    primary key (emp_id)
);