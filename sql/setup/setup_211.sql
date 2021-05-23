

CREATE procedure [dbo].[requirements_ReadAll]
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY
		select * from requirements

		
		RETURN(1);

	END TRY

	BEGIN CATCH


		RETURN(-1);

	END CATCH