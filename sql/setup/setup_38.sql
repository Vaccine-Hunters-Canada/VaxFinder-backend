
CREATE procedure [dbo].[organizations_GetOrganization] 
(
	@organizationID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		BEGIN TRANSACTION;
			select * from organizations where id = @organizationID

		COMMIT TRANSACTION;
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH