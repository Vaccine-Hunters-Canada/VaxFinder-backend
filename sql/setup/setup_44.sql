

CREATE procedure [dbo].[requirements_Update] 
(
	@requirementID int,
	@name varchar(255),
	@description varchar(255),
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
			update dbo.[requirements] set [name] = @name, [description] = @description
			where id = @requirementID

		COMMIT TRANSACTION;
		
		RETURN(@requirementID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH