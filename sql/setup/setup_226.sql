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