-- we don't know how to generate root <with-no-name> (class Root) :(
create table address
(
	id int identity
		constraint PK__address__3213E83FCFA7B88B
			primary key,
	line1 varchar(255),
	line2 varchar(255),
	city varchar(255),
	province nvarchar(255) not null
		constraint CK__address__provinc__6D0D32F4
			check ([province]='saskatchewan' OR [province]='quebec' OR [province]='prince_edward_island' OR [province]='ontario' OR [province]='nunavut' OR [province]='nova_scotia' OR [province]='northwest_territories' OR [province]='newfoundland_and_labrador' OR [province]='new_brunswick' OR [province]='manitoba' OR [province]='british_columbia' OR [province]='alberta'),
	postcode varchar(6) not null,
	location geography,
	created_at datetime constraint DF_address_created_at default getdate() not null
)