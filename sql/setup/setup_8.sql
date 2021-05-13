
create table postal_geo
(
	postal nchar(3) not null
		constraint PK_postal_geo
			primary key,
	area nchar(255) not null,
	province nchar(255) not null,
	lat decimal(10,6) not null,
	lon decimal(10,6) not null,
	geohash geography
)