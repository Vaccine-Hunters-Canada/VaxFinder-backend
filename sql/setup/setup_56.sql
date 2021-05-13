


CREATE procedure [dbo].[vaccine_availability_children_Update] 
(	
	@id uniqueidentifier,
	@time datetime,
	@taken_at datetime,
    @auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

    declare @valid bit
    declare @location int

    select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_children on vaccine_availability_children.vaccine_availability = vaccine_availability.id where vaccine_availability_children.id = @id
    select @valid = dbo.ValidateLocationKey(@auth, @location)

    if @valid = 0
    BEGIN
        return(0);
    END
	
	BEGIN TRY

		BEGIN TRANSACTION;
			UPDATE [dbo].[vaccine_availability_children]
			SET [time] = @time,  [taken_at] = @taken_at				
			WHERE id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH