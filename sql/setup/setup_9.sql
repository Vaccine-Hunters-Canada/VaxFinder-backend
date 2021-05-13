
create table requirements
(
	id int identity
		primary key,
	name varchar(255) not null,
	description varchar(255) not null,
	created_at datetime constraint DF_requirements_created_at default getdate() not null
)