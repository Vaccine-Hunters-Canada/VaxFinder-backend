


CREATE procedure [dbo].[security_Read] 
(
	@securityID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

			select * from dbo.[security] where id = @ID

		
		RETURN(@securityID);

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH