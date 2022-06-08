CREATE TABLE leituras ( 
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	timestamp DATETIME  NOT NULL,
	instance INTEGER  NOT NULL,
	resource varchar(8) NOT NULL,
	value REAL NOT NULL,
	status INTEGER NOT NULL,
	FOREIGN KEY(instance) REFERENCES instance(instance_number)
);

-- [1 - Plantação 1, 2 - Plantação 2, 3 - Plantação 3]
-- [Horta 1, Horta 2]
CREATE TABLE instances (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	instance_number INTEGER not null,
	status INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX instance_idx ON instance (instance_number);

CREATE TABLE resources (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	resource_number INTEGER 
		CHECK( resource_number IN (3303, 3304) ) not null,
	status INTEGER NOT NULL DEFAULT 1,
	normal INTEGER NOT NULL DEFAULT 1,
);


CREATE INDEX resource_idx ON instances (instance_number);

-- Python
-- [(3304, 'Umidade do Ar'), (3304, 'Temperatura')]

-- 1 para 1 -> escolhe onde vai a FK
-- 1 para N -> FK vai no N

-- N Instâncias para N Recursos (Implementar depois)