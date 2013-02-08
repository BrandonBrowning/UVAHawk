UVAHawk
=======

UVAHawk is a tool to assist the University of Akron's Association for Computing Machinery (ACMUA) chapter, specifically for SIGCOMP Programming Competition practices.
It scrapes the UVA Online Judge system's user history for members of ACMUA SIGCOMP, and reports on their progress on the problems assigned for the next friday.

UVAHawk is configured through a folder aptly named "config" as a sibling of the main executable script.  Here's an example structure.

    uvahawk.py
    config/
        user_map.csv
        problems/
        	2013-02-08.csv
        	2013-02-15.csv

user_map.csv
============
user_map.csv is a file containing the details of each person to report on.  Here's an example.

	name,uanetid,uvaid
	John Doe,foo12,130000
	Some Guy,wtf42,123210

The header line should be included, and unchanged.  This may be altered in the future.

Problem Files
=============
Each of the problems files should be named as an iso date of the friday the problems are to be gone over.  The format is as follows.

	problemid
	1
	42
	3
	101

Again, keep the header for now.

TODO
====
Say where the id's come from