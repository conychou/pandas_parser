# pandas_parser

This is a pandas wrapper to let user can call through API.

How to run
===================================================================
Please run in Linux environment
1. git clone https://github.com/conychou/pandas_parser.git
2. cd pandas_parser/
3. module load python-3.6
4. python3
5. exec(open("./compiler.py").read())
6. you can start playing with commands.

**For input command, please give the command in _statement_, 
(variable) := function(variable)**

**You can check result by type variable name**

Following is an inputfromfile function and result example.

    pd >> R := inputfromfile(sales)

    pd >> R

        saleid   itemid   customerid  storeid  time  qty   pricerange

    0       45  item133    customer2  store63    49   23   outrageous

    1      658   item75    customer2  store89    46   43   outrageous

    2      149  item103    customer2  store23    67    2        cheap

    3      398   item82    customer2  store41     3   27   outrageous

    ....


Supported Functions: 
===================================================================
// import vertical bar delimited of sales file. Suppose column headers are saleid|itemid|customerid|storeid|time|qty|pricerange

**R := inputfromfile(sales)**

// select rows of R whose time > 50 and qty < 30)

**R1 := select(R, (time > 50) and (qty < 30))** 

// select rows of R whose time > 50

**R8 := select(R, time > 50)**

// if selection filter is string and it’s not any of the column name, please add quotation marks

**R9 := select(R, pricerange = "outrageous")**	

// get columns saleid, qty, customerid and pricerange of the rows of R1 

**R2 := project(R1, saleid, qty, customerid, pricerange)**

// get average value of qty of R1

**R3 := avg(R1, qty)**

// select time, sum group by qty of R1

**R4 := sumgroup(R1, time, qty)**

// select qty and sum group by time,pricerange of R1 

**R5 := sumgroup(R1, qty, time, pricerange)**

// select qty and avg group by pricerange of R1

**R6 := avggroup(R1, qty, pricerange)**

// import vertical bar delimited of sales2 file. Suppose column headers are saleid|I|C|S|T|Q|P

**S := inputfromfile(sales2)**

// T has all the columns of R and S that R_saleid = S_C. The column headers
// are prefaced by the table they came from, e.g. R_saleid, R_qty, 
// R_customerid, R_pricerange, S_saleid, S_I, S_C, S_S, S_T, S_Q, S_P

**T := join(R, S, R_saleid = S_C)**

**T1 := join(R1, S, R1_qty <= S_Q)**

// sort T1 by S_C

**T2 := sort(T1, S_C)**

// sort T1 by R1_itemid, S_C (in that order)

**T2prime := sort(T1, R1_time, S_C)**

// perform the three item moving average of T2

**T3 := movavg(T2, R1_qty, 3)**

// perform the five item moving sum of T2

**T4 := movsum(T2, R1_qty, 5)**

// there is no index to use

**Q1 := select(S, saleid = 93086)**

// create an index on S based on column saleid

**Btree(S, saleid)**

// this should use the index Btree(S,saleid)

**Q2 := select(S, saleid = 93086)**

// this should not use an index Btree(S,saleid)

**Q3 := select(S, Q > 20)**

**Hash(S, saleid)**

// concatenate the two tables (must have the same schema)

**Q5 := concat(Q2, Q3)**

// export Q5 to bar file with vertical bar delimiter. 

**outputtofile(Q5, bar)**
