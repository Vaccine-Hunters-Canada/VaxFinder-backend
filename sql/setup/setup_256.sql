


CREATE procedure [dbo].[vaccine_availability_timeslots_ReadByParent]
(	
	@parentID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	declare @location int

	BEGIN TRY
			select * from dbo.vaccine_availability_timeslots where vaccine_availability_timeslots.vaccine_availability = @parentID
		
		RETURN(1);

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH