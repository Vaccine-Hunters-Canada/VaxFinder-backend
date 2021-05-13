

CREATE procedure [dbo].[requirements_Read] 
(
	@requirementID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from requirements where id = @requirementID

		COMMIT TRANSACTION;
		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH