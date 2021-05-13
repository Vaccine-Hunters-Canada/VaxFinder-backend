


CREATE procedure [dbo].[vaccine_availability_children_Create]
(	
	@parentID uniqueidentifier,
	@time datetime,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	declare @location int

	BEGIN TRY

		declare @valid bit

		select @location = [location] from dbo.vaccine_availability where dbo.vaccine_availability.id = @parentID

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END


		BEGIN TRANSACTION;
			INSERT INTO [dbo].[vaccine_availability_children]
           ([id]
		   ,[vaccine_availability]
           ,[time])
		VALUES
           (@ID
		   ,@parentID
           ,@time)

		Select @ID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH