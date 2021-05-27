CREATE procedure [dbo].[organizations_Update] 
(
	@organizationID int,
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
			update dbo.organizations set full_name = @full_name, short_name = @short_name, [description] = @description, [url] = @url where id = @organizationID
		COMMIT TRANSACTION;
		
		RETURN(@organizationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH