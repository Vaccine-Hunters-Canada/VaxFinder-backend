-- =============================================
-- Author:     Evan Gamble
-- Create Date: 2021-05-22
-- Description: Delete Organization Data
-- =============================================
CREATE PROCEDURE [dbo].[NukeOrg]
(
    @organizationID int
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON	
	

	BEGIN TRY
		BEGIN TRANSACTION
			delete from dbo.vaccine_availability_requirements where vaccine_availability in (select id from vaccine_availability where location in (select id from dbo.locations where organization = @organizationID))
			delete from dbo.vaccine_availability_timeslots where vaccine_availability in (select id from vaccine_availability where location in (select id from dbo.locations where organization = @organizationID))
			delete from dbo.vaccine_availability where location in (select id from dbo.locations where organization = @organizationID)
			delete from dbo.location_keys where location in (select id from dbo.locations where organization = @organizationID)
			delete from dbo.[address] where id in (select [address] from dbo.locations where organization = @organizationID)
			delete from dbo.locations where organization = @organizationID
		COMMIT TRANSACTION;
		
		return (1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH

END