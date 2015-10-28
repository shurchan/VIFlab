LOAD DATA local INFILE '/Users/misc/code/viflab/tests/aaa.csv'
#LOAD DATA local INFILE "aaa.csv"
    INTO TABLE testdb.AnnualData
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
