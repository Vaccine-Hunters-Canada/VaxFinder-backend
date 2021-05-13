

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