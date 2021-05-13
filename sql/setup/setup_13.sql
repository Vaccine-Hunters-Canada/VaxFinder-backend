
create table vaccines
(
	id int identity
		primary key,
	name varchar(50) not null,
	description varchar(255) not null,
	code varchar(2),
	created_at datetime constraint DF_vaccines_created_at default getdate() not null
)