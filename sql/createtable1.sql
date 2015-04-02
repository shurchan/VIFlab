/*create database testdb;
use testdb;
CREATE TABLE books (
     book_id INT,
     title VARCHAR(50),
     author VARCHAR(50));
*/
use testdb;
'describe books;'

CREATE TABLE IF NOT EXISTS `testdb`.`testcsv` (
  `idtestcsv` INT NOT NULL AUTO_INCREMENT,
  `FieldName` VARCHAR(45) NULL,
  `year` VARCHAR(45) NULL,
  `data_value` VARCHAR(45) NULL,
  PRIMARY KEY (`idtestcsv`))
ENGINE = InnoDB


'DROP TABLE IF EXISTS testcsv;'

select * from testcsv