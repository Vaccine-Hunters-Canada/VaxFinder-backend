

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