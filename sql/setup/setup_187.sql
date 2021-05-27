CREATE procedure [dbo].[organizations_Create] 
(
	@full_name varchar(255),
	@short_name varchar(50),
	@description varchar(2000),
	@url varchar(255),
	@auth uniqueidentifier
)
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
			INSERT INTO [dbo].[organizations]
			   ([full_name]
			   ,[short_name]
			   ,[description]
			   ,[url])
			VALUES
           (@full_name, @short_name, @description, @url)

		COMMIT TRANSACTION;

		SELECT @ID = SCOPE_IDENTITY()

		RETURN(@ID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH