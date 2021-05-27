
CREATE procedure [dbo].[keys_Read] 
(
	@key uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		
			select * from keys where id=@key

		
		
		return(1)

	END TRY

	BEGIN CATCH


		return(-1)

	END CATCH