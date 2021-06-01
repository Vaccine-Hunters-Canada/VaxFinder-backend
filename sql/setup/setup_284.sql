

create procedure [dbo].[security_Update] 
(
	@securityID int,
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
			update dbo.[security] set userName = @userName, [password] = @password, [key] = @key where id = @securityID

		COMMIT TRANSACTION;
		
		RETURN(@securityID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH