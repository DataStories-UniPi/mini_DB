create table joins (instructor.id str, instructor.name str, instructor.dept_name str, instructor.salary int, advisor.s_id str, advisor.i_id str);
insert into joins values(10101,srinivasan,comp. sci.,65000,12345,10101)
insert into joins values(22222,einstein,physics,95000,44553,22222)
insert into joins values(22222,einstein,physics,95000,45678,22222)
insert into joins values(45565,katz,comp. sci.,75000,00128,45565)
insert into joins values(45565,katz,comp. sci.,75000,76543,45565)
insert into joins values(76543,singh,finance,80000,23121,76543)
insert into joins values(76766,crick,biology,72000,98988,76766)
insert into joins values(98345,kim,elec. eng.,80000,76653,98345)
insert into joins values(98345,kim,elec. eng.,80000,98765,98345)
select * from instructor sm join advisor on id = i_id save as joinedTable2
compare joins with joinedTable2