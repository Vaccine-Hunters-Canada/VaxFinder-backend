CREATE procedure [dbo].[vaccine_availability_expanded_Create] 
(
	 @numberAvailable int
    ,@numberTotal int = null
    ,@date datetime
    ,@location int = null
    ,@vaccine int
    ,@inputType int
    ,@tagsA text = null
	,@line1 varchar(255)
    ,@line2 varchar(255)
    ,@city varchar(255)
    ,@province nvarchar(255)
    ,@postcode varchar(6)
    ,@latitude decimal(10,6) = null
	,@longitude decimal(10,6) = null
	,@name varchar(255)
	,@organization int
	,@phone varchar(255)
	,@notes text
	,@active bit	
	,@url varchar(255)
	,@tagsL text = null
	,@external_key varchar(255)	
	,@auth uniqueidentifier   
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()

	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return (-1)
		END

		declare @locationID int = 0
		declare @va uniqueidentifier = null
		declare @addressID int = 0
	
			
		if @location is null
			    select @locationID = id, @addressID = [address] from dbo.locations where TRIM(external_key) = trim(@external_key)
		else
		BEGIN
			select @locationID = id, @addressID = [address] from dbo.locations where id = @location

			if @locationID < 1
				return(-1)
		END		
		BEGIN TRANSACTION;
			if @locationID > 0
			BEGIN								

				EXECUTE @addressID = [dbo].[address_Update] 
									   @addressID
									  ,@line1
									  ,@line2
									  ,@city
									  ,@province
									  ,@postcode
									  ,@latitude
									  ,@longitude
									  ,@auth				

				update dbo.locations set [name] = @name, organization = @organization, phone = @phone, url = @url, notes = @notes, [address] = @addressID, active = @active, postcode = @postcode, tags = @tagsL, external_key=@external_key where id = @locationID

				select @va = id from dbo.vaccine_availability where location = @locationID and date = @date
				
				if @va is null
				BEGIN
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
					   ,@locationID
					   ,@vaccine
					   ,@inputType
					   ,@tagsA)

					SELECT * FROM dbo.vaccine_availability where vaccine_availability.id = @ID
				END
				ELSE
				BEGIN
					update dbo.[vaccine_availability] set numberAvailable = @numberAvailable, numberTotal = @numberTotal, [date] = @date, [location] = @locationID, vaccine = @vaccine, inputType = @inputType, tags = @tagsA where id = @VA

					SELECT * FROM dbo.vaccine_availability where vaccine_availability.id = @VA
				END
				
			END
			ELSE
			BEGIN			

				EXECUTE @addressID = [dbo].[address_Create] 
									   @line1
									  ,@line2
									  ,@city
									  ,@province
									  ,@postcode
									  ,@latitude
									  ,@longitude
									  ,@auth	

				EXECUTE @locationID = [dbo].[locations_Create] 
				   @name
				  ,@organization
				  ,@phone
				  ,@notes
				  ,@addressID
				  ,@active
				  ,@postcode
				  ,@url
				  ,@tagsL
				  ,@external_key
				  ,@auth
					

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
					   ,@locationID
					   ,@vaccine
					   ,@inputType
					   ,@tagsA)

				SELECT * FROM dbo.vaccine_availability where vaccine_availability.id = @ID

			END			

		COMMIT TRANSACTION;
		
		RETURN(@locationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-2);

	END CATCH
