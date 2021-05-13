
create table location_keys
(
	id int identity
		primary key,
	location int,
	[key] uniqueidentifier
)