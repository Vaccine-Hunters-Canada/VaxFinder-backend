


CREATE procedure [dbo].[security_Create] 
(
	@userName varchar(255),
	@password varchar(255),
	@key uniqueidentifier,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateAdminKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[security]
			([userName]
			,[password]
			,[key])
		VALUES
           (@userName,
		    @password,
		    @key)

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