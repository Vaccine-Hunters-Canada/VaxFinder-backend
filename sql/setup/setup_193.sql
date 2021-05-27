CREATE procedure [dbo].[organizations_Read] 
(
	@organizationID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

	
			select * from organizations where id = @organizationID

	
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH


		RETURN(-1);

	END CATCH