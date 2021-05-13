
create table vaccine_availability_children
(
	id uniqueidentifier not null
		constraint PK__entry_ch__3213E83F364F5FA4
			primary key,
	vaccine_availability uniqueidentifier not null,
	time datetime not null,
	taken_at datetime,
	created_at datetime constraint DF_entry_children_created_at default getdate() not null
)