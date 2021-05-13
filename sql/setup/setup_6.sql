
create table organizations
(
	id int identity
		constraint PK__organiza__3213E83FB21EF2A6
			primary key,
	full_name varchar(255),
	short_name varchar(50),
	description varchar(2000),
	url varchar(255),
	created_at datetime constraint DF_organizations_created_at default getdate() not null
)