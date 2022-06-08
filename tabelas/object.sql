CREATE TABLE [object] ( 
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	timestamp DATETIME  NOT NULL,
	instance INTEGER  NOT NULL,
	resource varchar(8) NOT NULL,
	value REAL NOT NULL,
	status INTEGER NOT NULL
); 
