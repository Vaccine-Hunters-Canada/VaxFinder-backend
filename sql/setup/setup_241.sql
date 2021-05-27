


CREATE procedure [dbo].[vaccine_availability_requirements_ReadByParent]
(	
	@parentID uniqueidentifier
)
AS
	SET NOCOUNT ON;
	
	declare @location int

	BEGIN TRY

			 SELECT vars.*, reqs.name, reqs.description
			 FROM dbo.vaccine_availability_requirements vars
			 JOIN dbo.requirements reqs on vars.requirement = reqs.id

		RETURN(1);

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH