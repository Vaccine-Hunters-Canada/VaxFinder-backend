

CREATE procedure [dbo].[address_Delete] 
(
	@addressID int,
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
			delete from [address] where id = @addressID

		COMMIT TRANSACTION;
		
		RETURN(@addressID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH