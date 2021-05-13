

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