

CREATE procedure [dbo].[vaccine_availability_timeslots_Read]
(	
	@id uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

			select * from dbo.vaccine_availability_timeslots where vaccine_availability_timeslots.id = @id
		
		RETURN(1);

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH