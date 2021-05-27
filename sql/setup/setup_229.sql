CREATE procedure [dbo].[vaccine_availability_ReadByLocation] 
(
	@locationID int,
	@date datetime = '1900-01-01' 
)
AS
	SET NOCOUNT ON;
	
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability where [location] = @locationID and [date] >= @date

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH