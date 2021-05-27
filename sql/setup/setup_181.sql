CREATE procedure [dbo].[locations_Update] 
(
	@locationID int,
	@name varchar(255),
	@organization int,
	@phone varchar(255),
	@notes text,
	@address int,
	@active bit,
	@postcode varchar(6),
	@tags text,
	@url varchar(255),
	@external_key varchar(255) = null,
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
			update dbo.locations set [name] = @name, organization = @organization, phone = @phone, url = @url, notes = @notes, [address] = @address, active = @active, postcode = @postcode, tags = @tags, external_key=@external_key where id = @locationID

		COMMIT TRANSACTION;
		
		RETURN(@locationID);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH