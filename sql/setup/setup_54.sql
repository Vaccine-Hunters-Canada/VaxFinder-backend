


CREATE procedure [dbo].[vaccine_availability_children_Read]
(	
	@id uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

		BEGIN TRANSACTION;
			select * from dbo.vaccine_availability_children where vaccine_availability_children.id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH