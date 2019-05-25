# pandas_parser

This is a pandas wrapper to let user can call in SQL-liked API

1. git clone https://github.com/conychou/pandas_parser.git
2. cd pandas_parser/
3. module load python-3.6
4. python3
5. exec(open("./compiler.py").read())

Then, you can start playing with commands, such as

// import vertical bar delimited of sales file. suppose column headers are saleid|itemid|customerid|storeid|time|qty|pricerange

R := inputfromfile(sales) 

// select rows of R whose time val is greater than 50 or qty < 30

R1 := select(R, (time > 50) and (qty < 30)) 

// select rows of R whose time val is greater than 50

R8 := select(R, time > 50) 

// if selection filter is string and it’s not any of the column name, please add quotation marks

R9 := select(R, pricerange = "outrageous")		

// R1 gets columns saleid, qty, customerid and pricerange of the rows of R1 

R2 := project(R1, saleid, qty, customerid, pricerange)  

// average value of qty

R3 := avg(R1, qty) 

// select time, sum group by qty

R4 := sumgroup(R1, time, qty) 

// select qty, sum group by time,pricerange 

R5 := sumgroup(R1, qty, time, pricerange) 

// select qty, avg group by pricerange

R6 := avggroup(R1, qty, pricerange) 

// suppose column headers are saleid|I|C|S|T|Q|P

S := inputfromfile(sales2) 

// T has all the columns of R and S ,but the
// column headers are prefaced by the table they came from, e.g. R_saleid, R_qty, 
// R_customerid, R_pricerange, S_saleid, S_I, S_C, S_S, S_T, S_Q, S_P

T := join(R, S, R_saleid = S_C) 

T1 := join(R1, S, R1_qty <= S_Q)   

// sort T1 by S_C

T2 := sort(T1, S_C) 

// sort T1 by R1_itemid, S_C (in that order)

T2prime := sort(T1, R1_time, S_C) 

// perform the three item moving average of T2

T3 := movavg(T2, R1_qty, 3) 

// perform the five item moving sum of T2

T4 := movsum(T2, R1_qty, 5) 

// there is no index to use

Q1 := select(S, saleid = 93086) 

// create an index on S based on column saleid

Btree(S, saleid) 

// this should use the index Btree(S,saleid)

Q2 := select(S, saleid = 93086) 

// this should not use an index Btree(S,saleid)

Q3 := select(S, Q > 20) 

Hash(S, saleid)

// concatenate the two tables (must have the same schema)

Q5 := concat(Q2, Q3) 

outputtofile(Q5, bar)
