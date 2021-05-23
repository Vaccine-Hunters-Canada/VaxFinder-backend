
CREATE procedure [dbo].[keys_Update] 
(
	@key uniqueidentifier,
	@start_date datetime,
	@end_date datetime,
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
			update dbo.[keys] set [start_date] = @start_date, [end_date] = @end_date
			where id = @key

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH