

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