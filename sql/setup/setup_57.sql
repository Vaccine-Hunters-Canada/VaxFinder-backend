


CREATE procedure [dbo].[vaccine_availability_requirements_Create] 
(	
	@vaccine_availability uniqueidentifier,
	@requirement int,	
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	BEGIN TRY

		declare @location int
		declare @valid bit

		select @location = location from dbo.vaccine_availability where id = @vaccine_availability

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;	

			INSERT INTO [dbo].vaccine_availability_requirements
			   (id,
			   [vaccine_availability]
			   ,[requirement]
			   ,[active]
			   ,[created_at])
			VALUES
			   (@ID,
			   @vaccine_availability,
			   @requirement,
			   1,
			   GetDate())

		COMMIT TRANSACTION;
		
		Select @ID

		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH