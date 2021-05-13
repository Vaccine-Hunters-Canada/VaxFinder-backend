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
go

create table inputType
(
	ID int identity,
	InputType nchar(255)
)
go

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
go

create table location_keys
(
	id int identity
		primary key,
	location int,
	[key] uniqueidentifier
)
go

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
go

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
go

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
go

create table requirements
(
	id int identity
		primary key,
	name varchar(255) not null,
	description varchar(255) not null,
	created_at datetime constraint DF_requirements_created_at default getdate() not null
)
go

create table roles
(
	RoleType int identity,
	RoleName nchar(255)
)
go

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
go

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
go

create table vaccines
(
	id int identity
		primary key,
	name varchar(50) not null,
	description varchar(255) not null,
	code varchar(2),
	created_at datetime constraint DF_vaccines_created_at default getdate() not null
)
go

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
go

-- =============================================
-- Author:      Evan Gamble
-- Create Date: 2021-05-04
-- Description: From https://www.c-sharpcorner.com/UploadFile/afenster/how-to-find-a-doctor-near-your-home-in-sql-server/
-- =============================================
CREATE FUNCTION [dbo].[CalculateDistance]  
(  
    @lat1Degrees decimal(10,6),  
    @lon1Degrees decimal(10,6),  
   
    @lat2Degrees decimal(10,6),  
    @lon2Degrees decimal(10,6)  
)  
RETURNS decimal(9,4)  
AS  
BEGIN  
   
    DECLARE @earthSphereRadiusKilometers as decimal(10,6)  
    DECLARE @kilometerConversionToMilesFactor as decimal(7,6)  
    SELECT @earthSphereRadiusKilometers = 6366.707019  
    SELECT @kilometerConversionToMilesFactor = .621371  
   
    -- convert degrees to radians  
    DECLARE @lat1Radians decimal(10,6)  
    DECLARE @lon1Radians decimal(10,6)  
    DECLARE @lat2Radians decimal(10,6)  
    DECLARE @lon2Radians decimal(10,6)  
    SELECT @lat1Radians = (@lat1Degrees / 180) * PI()  
    SELECT @lon1Radians = (@lon1Degrees / 180) * PI()  
    SELECT @lat2Radians = (@lat2Degrees / 180) * PI()  
    SELECT @lon2Radians = (@lon2Degrees / 180) * PI()  
   
    -- formula for distance from [lat1,lon1] to [lat2,lon2]  
    RETURN ROUND(2 * ASIN(SQRT(POWER(SIN((@lat1Radians - @lat2Radians) / 2) ,2)  
        + COS(@lat1Radians) * COS(@lat2Radians) * POWER(SIN((@lon1Radians - @lon2Radians) / 2), 2)))  
        * (@earthSphereRadiusKilometers * @kilometerConversionToMilesFactor), 4)  
   
END
go

-- =============================================
-- Author:      Evan Gamble
-- Create Date: 04-30-2021
-- Description: Get all avaliable vaccines
-- =============================================
CREATE PROCEDURE [dbo].[GetAvailableVaccines]
(
    @postal varchar(6),
    @date datetime
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

        BEGIN TRY
            declare @lat decimal (10,6)
            declare @lon decimal (10,6)
            declare @radLat decimal (2,2)
            declare @radLon decimal (2,2)

            select @lat= postal_geo.lat, @lon = postal_geo.lon from dbo.postal_geo where postal_geo.postal = left(@postal,3)			

            set @radLat = 0.5
            set @radLon = 0.5
			
			select va.id, va.numberAvailable, va.numberTotal, va.[date], va.[location], va.[vaccine], va.[inputType], va.[tags], va.[created_at],  IDENTITY(INT, 1, 1) as [sort] into #vaccine_availability_temp 
			from dbo.vaccine_availability va join dbo.locations on va.[location] = locations.id
			where left([locations].postcode,3) in ( select PC.postal from dbo.postal_geo PC where (ABS(@lat - PC.Lat) < @radLat) and (ABS(@lon - PC.Lon) < @radLon) ) and  [date] > @date 
			order by [location], [date]


			select [location], [date], max(created_at) as [created_at] into #filter from #vaccine_availability_temp  group by [location], [date]
			
			--delete from #vaccine_availability_temp where id not in (select id from #filter f join #vaccine_availability_temp va on va.created_at = f.created_at AND va.location = f.location)

            -- vaccine_availability table
            SELECT va.id, va.numberAvailable, va.numberTotal, va.[date], va.[location], va.[vaccine], va.[inputType], va.[tags], va.[created_at] from #vaccine_availability_temp VA
            join 
                locations
                on [location] = [locations].id                       
			order by
				sort            

			select dbo.vaccine_availability_children.* from dbo.vaccine_availability_children join #vaccine_availability_temp on #vaccine_availability_temp.id = vaccine_availability_children.vaccine_availability
			order by
				sort
            
			select dbo.vaccine_availability_requirements.* from dbo.vaccine_availability_requirements join #vaccine_availability_temp on #vaccine_availability_temp.id = vaccine_availability_requirements.vaccine_availability
			order by
				sort
            
			select dbo.locations.* from dbo.locations join #vaccine_availability_temp on  #vaccine_availability_temp.[location] = locations.id
			order by
				sort
            
			select dbo.address.id, dbo.address.line1, dbo.address.line2, dbo.address.city, dbo.address.province, dbo.address.postcode, dbo.address.created_at from dbo.locations join #vaccine_availability_temp on #vaccine_availability_temp.[location] = locations.id join [address] on address.id = locations.[address]
			order by 
				sort            
			
			SELECT dbo.organizations.* from dbo.organizations join dbo.locations on locations.organization = organizations.id join #vaccine_availability_temp va on va.location = locations.id
			order by 
				sort    

			drop table #vaccine_availability_temp
			drop table #filter
        END TRY
        BEGIN CATCH

--          ==== Rollback transaction
            IF XACT_STATE() <> 0
                ROLLBACK TRANSACTION;

            RETURN(-1);

        END CATCH
END
go

-- =============================================
-- Author:      Evan Gamble	
-- Create Date: 05-03-2021
-- Description: Calculating a geohash based on lat/long
-- =============================================
CREATE FUNCTION GetGeoHash
(
    -- Add the parameters for the function here
   @latitude decimal(10,6),
   @longitude decimal(10,6)
)
RETURNS geography
AS
BEGIN
    declare @geographyPoint geography;

	select @geographyPoint = geography::Point(@latitude, @longitude, '4326');		

	return @geographyPoint
END
go

CREATE PROCEDURE [dbo].[GetVaccineLocationsNearby]
(
    @postal varchar(6),
    @date datetime
)
AS
BEGIN
    -- SET NOCOUNT ON is added to prevent extra result sets from interfering with SELECT statements.
    SET NOCOUNT ON
        BEGIN TRY
            DECLARE @lat decimal (10,6)
            DECLARE @lon decimal (10,6)
            DECLARE @radLat decimal (2,2)
            DECLARE @radLon decimal (2,2)

            SELECT @lat= postal_geo.lat, @lon = postal_geo.lon
            FROM dbo.postal_geo
            WHERE postal_geo.postal = left(@postal,3)

            SET @radLat = 0.5
            SET @radLon = 0.5

            -- Store locations near a postal code into a temporary table
            SELECT *
            INTO #locations_temp
            FROM dbo.locations l
            WHERE left(l.postcode, 3) IN (
                SELECT pc.postal FROM dbo.postal_geo pc
                WHERE (ABS(@lat - pc.Lat) < @radLat) AND (ABS(@lon - pc.Lon) < @radLon)
            )

            -- Select locations near a postal code
            SELECT * FROM #locations_temp

            -- Select organizations at locations near a postal code
            SELECT o.*
            FROM dbo.organizations o
            JOIN #locations_temp lt
                ON o.id = lt.organization

            -- Select addresses at locations near a postal code
            SELECT a.id, a.line1, a.line2, a.city, a.province, a.postcode, a.created_at
            FROM dbo.address a
            JOIN #locations_temp lt
                ON a.id = lt.address

            -- Store vaccine availabilities for locations near a postal code (and after @date) into a temporary table
            SELECT va.*,  IDENTITY(INT, 1, 1) as [selected_vaccine_availabilities]
            INTO #vaccine_availability_temp
            FROM dbo.vaccine_availability va
            JOIN #locations_temp
                ON #locations_temp.id = va.location AND va.date > @date
            ORDER BY va.date

            -- Select vaccine availabilities for locations near a postal code (and after @date)
            SELECT
                   vat.id,
                   vat.numberAvailable,
                   vat.numberTotal,
                   vat.date,
                   vat.location,
                   vat.vaccine,
                   vat.inputType,
                   vat.tags,
                   vat.created_at
            FROM #vaccine_availability_temp vat

            -- Select children (timeslots) for vaccine availabilities for locations near a postal code (and after @date)
            SELECT vac.*
            FROM dbo.vaccine_availability_children vac
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vac.vaccine_availability
            ORDER BY selected_vaccine_availabilities, vac.taken_at DESC, vac.time

            --- Select requirements for vaccine availabilities for locations near a postal code (and after @date)
            SELECT vars.*
            FROM dbo.vaccine_availability_requirements vars
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vars.vaccine_availability
            ORDER BY selected_vaccine_availabilities

            -- Drop temporary tables
            DROP TABLE #vaccine_availability_temp
            DROP TABLE #locations_temp
        END TRY
        BEGIN CATCH
            -- Rollback transaction
            IF XACT_STATE() <> 0
                ROLLBACK TRANSACTION;
            RETURN(-1);
        END CATCH
END
go

-- =============================================
-- Author:      Evan Gamble
-- Create Date: 2021-05-04
-- Description: From https://www.c-sharpcorner.com/UploadFile/afenster/how-to-find-a-doctor-near-your-home-in-sql-server/
-- =============================================
CREATE PROCEDURE [dbo].[PostalCodesNearLatLongAndRad]  
   
            @Latitude DECIMAL(10,6),  
            @Longitude DECIMAL(10,6),
			@LatRad DECIMAL(2,2),
			@LonRad DECIMAL(2,2)
AS  
BEGIN  
            SET NOCOUNT ON;  
            select distinct  
            PC.postal,
            PC.lat,
            PC.lon,
            dbo.CalculateDistance(@Latitude, @Longitude, PC.Lat, PC.Lon) as Distance            
            from dbo.postal_geo PC
            where (ABS(@Latitude - PC.Lat) < @LatRad)  -- Lines of latitude are ~69 miles apart.   
            and (ABS(@Longitude - PC.Lon) < @LonRad)  -- Lines of longitude in the U.S. are ~53 miles apart.            
			order by Distance
END
go



CREATE procedure [dbo].[TruncateTable] 
AS
	
	truncate table dbo.vaccine_availability_children
	truncate table dbo.vaccine_availability_requirements
	truncate table dbo.vaccine_availability
	truncate table dbo.location_keys
	truncate table dbo.locations
	truncate table dbo.[address]
	truncate table dbo.organizations
	truncate table dbo.requirements
	truncate table dbo.keys
	truncate table dbo.vaccines

go


CREATE FUNCTION [dbo].[ValidateAdminKey](@key uniqueidentifier)
RETURNS bit AS
BEGIN
    declare @role int
	select @role = [role] from dbo.keys where id = @key

	IF @role = 1
	BEGIN
		RETURN 1
	END

	RETURN 0
END
go

CREATE FUNCTION dbo.ValidateKey(@key uniqueidentifier, @location int)
RETURNS bit AS
BEGIN
    declare @role int
	select @role = [role] from dbo.keys where id = @key

	IF @role = 1
	BEGIN
		RETURN 1
	END
    
	IF @role = 2
	BEGIN
		RETURN 1
	END

	IF @role = 3
	BEGIN
		declare @count int
		set @count = 0

		select @count = count(*) from dbo.location_keys where [location] = @location and [key] = @key

		if @count > 0
		BEGIN
			return 1
		END

	END

	return 0
END
go


CREATE FUNCTION [dbo].[ValidateStaffKey](@key uniqueidentifier)
RETURNS bit AS
BEGIN
    declare @role int
	select @role = [role] from dbo.keys where id = @key

	IF @role = 1
	BEGIN
		RETURN 1
	END
    
	IF @role = 2
	BEGIN
		RETURN 1
	END

	RETURN 0
END
go


CREATE procedure [dbo].[address_Create] 
(
	@line1 varchar(255),
    @line2 varchar(255),
    @city varchar(255),
    @province nvarchar(255),
    @postcode varchar(6),
    @latitude decimal(10,6) = null,
	@longitude decimal(10,6) = null,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			DECLARE @geographyPoint geography

			select @geographyPoint = dbo.GetGeoHash(@latitude, @longitude)

			if (@latitude is not null)
				begin
					if (@longitude is not null)
					begin
						select @geographyPoint = geography::Point(@latitude, @longitude, '4326');						
						
						INSERT INTO [dbo].[address]
							   ([line1]
							   ,[line2]
							   ,[city]
							   ,[province]
							   ,[postcode]
							   ,[location])
						 VALUES
							   (@line1,
								@line2,
							   @city,
							   @province,
							   @postcode,
							   @geographyPoint)
					end
					else
						begin					
							INSERT INTO [dbo].[address]
							   ([line1]
							   ,[line2]
							   ,[city]
							   ,[province]
							   ,[postcode]
							   ,[location])
							VALUES
							   (@line1,
								@line2,
							   @city,
							   @province,
							   @postcode,
							   null)
						end
					end
				else
					begin					
						INSERT INTO [dbo].[address]
						   ([line1]
						   ,[line2]
						   ,[city]
						   ,[province]
						   ,[postcode]
						   ,[location])
						VALUES
						   (@line1,
							@line2,
						   @city,
						   @province,
						   @postcode,
						   null)
					end

		SELECT @ID = SCOPE_IDENTITY()

		COMMIT TRANSACTION;
		
		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[address_Delete_Key] 
(
	@addressID int,
	@auth uniqueidentifier 
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END


		BEGIN TRANSACTION;
			delete from [address] where id = @addressID

		COMMIT TRANSACTION;
		
		RETURN(@addressID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[address_Read] 
(
	@addressID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select id, line1, line2, city, province, postcode, created_at from address where id = @addressID

		COMMIT TRANSACTION;
		
		RETURN(@addressID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[address_Update] 
(
	@addressID int,
	@line1 varchar(255),
    @line2 varchar(255),
    @city varchar(255),
    @province nvarchar(255),
    @postcode varchar(6),
	@latitude decimal(10,6),
	@longitude decimal(10,6),
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			DECLARE @geographyPoint geography
			select @geographyPoint = dbo.GetGeoHash(@latitude, @longitude)

			update dbo.[address] set line1=@line1, line2 = @line2, city = @city, province = @province, postcode = @postcode, [location] = @geographyPoint
			where id = @addressID

		COMMIT TRANSACTION;
		
		RETURN(@addressID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[keys_Create] 
(
	@start_date datetime,
	@end_date datetime,
	@role int,
	@auth uniqueidentifier)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	BEGIN TRY		

		declare @valid bit

		select @valid = dbo.ValidateAdminKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[keys]
           ([id]
           ,[start_date]
           ,[end_date]
           ,[role])
		VALUES
           (@ID
           ,@start_date
           ,@end_date
           ,@role)		

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[keys_Read] 
(
	@key uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from keys where id=@key

		COMMIT TRANSACTION;
		
		return(1)

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		return(-1)

	END CATCH
go


CREATE procedure [dbo].[keys_Update] 
(
	@key uniqueidentifier,
	@start_date datetime,
	@end_date datetime,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY
		
		declare @valid bit

		select @valid = dbo.ValidateAdminKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END


		BEGIN TRANSACTION;
			update dbo.[keys] set [start_date] = @start_date, [end_date] = @end_date
			where id = @key

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[location_keys_Create] 
(
	@location int,	
	@key uniqueidentifier,
	@auth uniqueidentifier)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY		
		
		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[location_keys]
				([location]
				,[key])
			VALUES
           (@location,@key)

		SELECT @ID = SCOPE_IDENTITY()

		COMMIT TRANSACTION;
		
		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[locations_Create] 
(
	@name varchar(255),
	@organization int,
	@phone varchar(255),
	@notes text,
	@address int,
	@active bit,
	@postcode varchar(6),
	@url varchar(255),
	@tags text,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[locations]
           ([name]
           ,[organization]
           ,[phone]
           ,[notes]
           ,[address]
           ,[active]
           ,[postcode]
		   ,[url]
		   ,[tags])
     VALUES
           (@name
           ,@organization
           ,@phone
           ,@notes 
           ,@address
           ,@active
           ,@postcode
		   ,@url
		   ,@tags)

		SELECT @ID = SCOPE_IDENTITY()

		COMMIT TRANSACTION;
		
		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[locations_Delete] 
(
	@locationID int,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			delete from locations where id = @locationID

		COMMIT TRANSACTION;
		
		RETURN(@locationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[locations_Read] 
(
	@locationID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from locations where id = @locationID

		COMMIT TRANSACTION;
		
		RETURN(@locationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[locations_Update] 
(
	@locationID int,
	@name varchar(255),
	@organization int,
	@phone varchar(255),
	@notes text,
	@address int,
	@active bit,
	@postcode varchar(6),
	@tags text,
	@url varchar(255),
	@auth uniqueidentifier = null
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			update dbo.locations set [name] = @name, organization = @organization, phone = @phone, url = @url, notes = @notes, [address] = @address, active = @active, postcode = @postcode, tags = @tags where id = @locationID

		COMMIT TRANSACTION;
		
		RETURN(@locationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[organizations_Create] 
(
	@full_name varchar(255),
	@short_name varchar(50),
	@description varchar(2000),
	@url varchar(255),
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY
		
		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[organizations]
			   ([full_name]
			   ,[short_name]
			   ,[description]
			   ,[url])
			VALUES
           (@full_name, @short_name, @description, @url)

		COMMIT TRANSACTION;

		SELECT @ID = SCOPE_IDENTITY()

		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[organizations_Delete] 
(
	@organizationID int,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

	declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			delete from organizations where id = @organizationID

		COMMIT TRANSACTION;
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[organizations_GetOrganization] 
(
	@organizationID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from organizations where id = @organizationID

		COMMIT TRANSACTION;
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[organizations_Update] 
(
	@organizationID int,
	@full_name varchar(255),
	@short_name varchar(50),
	@description varchar(2000),
	@url varchar(255),
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			update dbo.organizations set full_name = @full_name, short_name = @short_name, [description] = @description, [url] = @url where id = @organizationID
		COMMIT TRANSACTION;
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[requirements_Create] 
(
	@name varchar(255),
	@description varchar(255),
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[requirements]
			([name]
			,[description])
		VALUES
           (@name, 
		    @description)

		SELECT @ID = SCOPE_IDENTITY()

		COMMIT TRANSACTION;
		
		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[requirements_Delete] 
(
	@requirementID int,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			delete from [requirements] where id = @requirementID

		COMMIT TRANSACTION;
		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[requirements_Read] 
(
	@requirementID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from requirements where id = @requirementID

		COMMIT TRANSACTION;
		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[requirements_ReadAll]
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from requirements

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[requirements_Update] 
(
	@requirementID int,
	@name varchar(255),
	@description varchar(255),
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			update dbo.[requirements] set [name] = @name, [description] = @description
			where id = @requirementID

		COMMIT TRANSACTION;
		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

-- =============================================
-- Author:      <Author, , Name>
-- Create Date: <Create Date, , >
-- Description: <Description, , >
-- =============================================
CREATE PROCEDURE dbo.test
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

	select * from dbo.locations join dbo.address on locations.address = address.id

	select * from dbo.vaccine_availability

	return(1)
END
go

-- =============================================
-- Author:      Alvin
-- =============================================
CREATE PROCEDURE dbo.testingstuff
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

	select id from dbo.address
	select id from dbo.vaccine_availability

	return(-1)
END
go

-- =============================================
-- Author:		Evan Gamble
-- Create date: 2021-04-05
-- Description:	Function call
-- =============================================
CREATE FUNCTION udfGetPostCodesNearMe (
    @Latitude DECIMAL(10,6),  
    @Longitude DECIMAL(10,6),
	@LatRad DECIMAL(2,2),
	@LonRad DECIMAL(2,2)
)
RETURNS TABLE
AS
RETURN     
    select distinct  
    PC.postal    
    from dbo.postal_geo PC
    where (ABS(@Latitude - PC.Lat) < @LatRad)  -- Lines of latitude are ~69 miles apart.   
    and (ABS(@Longitude - PC.Lon) < @LonRad)  -- Lines of longitude in the U.S. are ~53 miles apart.            
go



CREATE procedure [dbo].[vaccine_availability_Create_Key] 
(
	@numberAvailable int
    ,@numberTotal int = null
    ,@date datetime
    ,@location int
    ,@vaccine int
    ,@inputType int
    ,@tags text = null
	,@auth uniqueidentifier   
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()

	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;		

			INSERT INTO [dbo].[vaccine_availability]
           ([id]
		   ,[numberAvailable]
           ,[numberTotal]
           ,[date]
           ,[location]
           ,[vaccine]
           ,[inputType]
           ,[tags])
     VALUES
           (@ID
		   ,@numberAvailable
           ,@numberTotal
           ,@date
           ,@location
           ,@vaccine
           ,@inputType
           ,@tags)

		Select @ID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_Delete] 
(
	@avaliabilityID uniqueidentifier,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

	BEGIN TRY

		BEGIN TRANSACTION;

			declare @valid bit
			declare @location int
			
			select @location = vaccine_availability.location from dbo.vaccine_availability where vaccine_availability.id = @avaliabilityID

			select @valid = dbo.ValidateLocationKey(@auth, @location)

			if @valid = 0
			BEGIN
				return(0);
			END
			
			delete from vaccine_availability where id = @avaliabilityID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

CREATE procedure [dbo].[vaccine_availability_Read] 
(
	@availabilityID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability where id = @availabilityID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go


CREATE procedure [dbo].[vaccine_availability_Update] 
(
	@id uniqueidentifier
	,@numberAvailable int
    ,@numberTotal int
    ,@date datetime
    ,@location int
    ,@vaccine int
    ,@inputType int
    ,@tags text
    ,@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

	BEGIN TRY

        declare @valid bit

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			update dbo.[vaccine_availability] set numberAvailable = @numberAvailable, numberTotal = @numberTotal, [date] = @date, [location] = @location, vaccine = @vaccine, inputType = @inputType, tags = @tags where id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_children_Create]
(	
	@parentID uniqueidentifier,
	@time datetime,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	declare @location int

	BEGIN TRY

		declare @valid bit

		select @location = [location] from dbo.vaccine_availability where dbo.vaccine_availability.id = @parentID

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END


		BEGIN TRANSACTION;
			INSERT INTO [dbo].[vaccine_availability_children]
           ([id]
		   ,[vaccine_availability]
           ,[time])
		VALUES
           (@ID
		   ,@parentID
           ,@time)

		Select @ID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go




CREATE procedure [dbo].[vaccine_availability_children_Delete] 
(
	@id uniqueidentifier,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

	BEGIN TRY

		BEGIN TRANSACTION;

			declare @valid bit
			declare @location int
			
			select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_children on vaccine_availability_children.vaccine_availability = vaccine_availability.id where vaccine_availability_children.id = @id

			select @valid = dbo.ValidateLocationKey(@auth, @location)

			if @valid = 0
			BEGIN
				return(0);
			END
			
			delete from vaccine_availability_children where id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_children_Read]
(	
	@id uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_children where vaccine_availability_children.id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go




create procedure [dbo].[vaccine_availability_children_ReadByParent]
(	
	@parentID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_children where vaccine_availability_children.vaccine_availability = @parentID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_children_Update] 
(	
	@id uniqueidentifier,
	@time datetime,
	@taken_at datetime,
    @auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

    declare @valid bit
    declare @location int

    select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_children on vaccine_availability_children.vaccine_availability = vaccine_availability.id where vaccine_availability_children.id = @id
    select @valid = dbo.ValidateLocationKey(@auth, @location)

    if @valid = 0
    BEGIN
        return(0);
    END
	
	BEGIN TRY

		BEGIN TRANSACTION;
			UPDATE [dbo].[vaccine_availability_children]
			SET [time] = @time,  [taken_at] = @taken_at				
			WHERE id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_requirements_Create] 
(	
	@vaccine_availability uniqueidentifier,
	@requirement int,	
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	BEGIN TRY

		declare @location int
		declare @valid bit

		select @location = location from dbo.vaccine_availability where id = @vaccine_availability

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;	

			INSERT INTO [dbo].vaccine_availability_requirements
			   (id,
			   [vaccine_availability]
			   ,[requirement]
			   ,[active]
			   ,[created_at])
			VALUES
			   (@ID,
			   @vaccine_availability,
			   @requirement,
			   1,
			   GetDate())

		COMMIT TRANSACTION;
		
		Select @ID

		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go





CREATE procedure [dbo].[vaccine_availability_requirements_Delete] 
(
	@id uniqueidentifier,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

	BEGIN TRY

		BEGIN TRANSACTION;

			declare @valid bit
			declare @location int
			
			select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_requirements on vaccine_availability_requirements.vaccine_availability = vaccine_availability.id where vaccine_availability_requirements.id = @id

			select @valid = dbo.ValidateLocationKey(@auth, @location)

			if @valid = 0
			BEGIN
				return(0);
			END
			
			delete from vaccine_availability_requirements where id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go




CREATE procedure [dbo].[vaccine_availability_requirements_Read]
(	
	@id uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_requirements where vaccine_availability_requirements.id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go




CREATE procedure [dbo].[vaccine_availability_requirements_ReadByParent]
(	
	@parentID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_requirements where vaccine_availability_requirements.vaccine_availability = @parentID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go



CREATE procedure [dbo].[vaccine_availability_requirements_Update] 
(	
	@id uniqueidentifier,
	@requirement int,
	@active bit,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	BEGIN TRY

		declare @location int
		declare @valid bit

		select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_requirements on vaccine_availability_requirements.vaccine_availability = vaccine_availability.id where vaccine_availability_requirements.id = @id

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END


		BEGIN TRANSACTION;

			update [dbo].vaccine_availability_requirements
			set [requirement] = @requirement, [active] = @active
			where id= @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH
go

