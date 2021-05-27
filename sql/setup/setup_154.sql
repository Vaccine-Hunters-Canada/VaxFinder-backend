
CREATE procedure [dbo].[keys_Create] 
(
	@start_date datetime,
	@end_date datetime,
	@role int,
	@auth uniqueidentifier)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()
	BEGIN TRY		

		declare @valid bit

		select @valid = dbo.ValidateAdminKey(@auth)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;
			INSERT INTO [dbo].[keys]
           ([id]
           ,[start_date]
           ,[end_date]
           ,[role])
		VALUES
           (@ID
           ,@start_date
           ,@end_date
           ,@role)		

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH