



create procedure [dbo].[vaccine_availability_children_ReadByParent]
(	
	@parentID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_children where vaccine_availability_children.vaccine_availability = @parentID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH