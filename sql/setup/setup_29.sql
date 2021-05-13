

CREATE procedure [dbo].[keys_Read] 
(
	@key uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from keys where id=@key

		COMMIT TRANSACTION;
		
		return(1)

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		return(-1)

	END CATCH