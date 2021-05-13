
create table vaccine_availability
(
	id uniqueidentifier constraint DF_vaccine_avaliability_id default newid() not null
		constraint PK__entries__3213E83F89BAFED2
			primary key,
	numberAvailable int not null,
	numberTotal int,
	date datetime not null,
	location int not null
		constraint FK__entries__locatio__7B5B524B
			references locations,
	vaccine int
		constraint FK__entries__vaccine__7C4F7684
			references vaccines,
	inputType int not null,
	tags text,
	created_at datetime constraint DF_entries_created_at default getdate() not null
)