

CREATE procedure [dbo].[location_keys_Create] 
(
	@location int,	
	@key uniqueidentifier,
	@auth uniqueidentifier)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY		
		
		declare @valid bit

		select @valid = dbo.ValidateStaffKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[location_keys]
				([location]
				,[key])
			VALUES
           (@location,@key)

		SELECT @ID = SCOPE_IDENTITY()

		COMMIT TRANSACTION;
		
		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH