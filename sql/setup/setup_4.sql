
create table keys
(
	id uniqueidentifier constraint DF_keys_id default newid() not null
		constraint PK__keys__3213E83F54969EF5
			primary key,
	start_date datetime not null,
	end_date datetime not null,
	role nvarchar(255) not null,
	created_at datetime constraint DF_keys_created_at default getdate() not null
)