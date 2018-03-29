BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `newtable` (
no integer primary key,
mon varchar(100),
tue varchar(100),
wed varchar(100),
thu varchar(100),
fri varchar(100),
sat varchar(100),
sun varchar(50)
);
COMMIT;