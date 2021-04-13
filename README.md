# Parse-GEDCOM
A script to parse the data from a .ged file.

A Command line program which discover errors and anomalies in GEDCOM genealogy files

GEDCOM is a standard format for genealogy data developed by The Church of Jesus Christ of Latter-day Saints. GEDCOM identifies two major entities: individuals and families. GEDCOM allows you to describe the following characteristics of individuals:

•Unique individual ID

•Name

•Sex/Gender

•Birth date

•Death date

•Unique Family ID where the individual is a child

•Unique Family ID where the individual is a spouseLikewise,

GEDCOM allows you to describe the following characteristics of a family:

•Unique family ID

•Unique individual ID of husband

•Unique individual ID of wife

•Unique individual ID of each child in the family

•Marriage date

•Divorce date,

if appropriateGEDCOMis a line-oriented text file format where each line has three parts separated by blank space:

1.level number(0, 1, or 2)

2.tag(a string of 3 or 4 characters)

3.arguments(an optional character string)
