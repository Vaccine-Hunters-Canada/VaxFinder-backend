


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