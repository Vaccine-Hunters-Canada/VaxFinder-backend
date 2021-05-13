

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