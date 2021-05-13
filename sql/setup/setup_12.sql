
create table vaccine_availability_requirements
(
	id uniqueidentifier not null
		constraint PK__entry_re__3213E83F21B23394
			primary key,
	vaccine_availability uniqueidentifier not null,
	requirement int not null,
	active bit constraint DF_entry_requirements_active default 1 not null,
	created_at datetime not null
)