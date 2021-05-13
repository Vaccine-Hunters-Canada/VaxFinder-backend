


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