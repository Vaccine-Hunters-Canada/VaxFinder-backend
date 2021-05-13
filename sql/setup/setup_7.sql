
create table locations
(
	id int identity
		constraint PK__location__3213E83F9A5A87D6
			primary key,
	name varchar(255) not null,
	organization int
		constraint FK__locations__organ__656C112C
			references organizations,
	phone varchar(255),
	notes text,
	address int
		constraint FK__locations__addre__7A672E12
			references address,
	active bit constraint DF__locations__activ__5EBF139D default 1 not null,
	postcode varchar(6),
	url varchar(255),
	tags text,
	created_at datetime constraint DF_locations_created_at default getdate() not null
)