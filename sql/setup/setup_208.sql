
CREATE procedure [dbo].[requirements_Read] 
(
	@requirementID int
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

			select * from requirements where id = @requirementID

		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH