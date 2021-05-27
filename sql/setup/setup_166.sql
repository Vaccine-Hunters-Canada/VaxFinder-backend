
CREATE procedure [dbo].[locations_Create] 
(
	@name varchar(255),
	@organization int,
	@phone varchar(255),
	@notes text,
	@address int,
	@active bit,
	@postcode varchar(6),
	@url varchar(255),
	@tags text,
	@external_key varchar(255) = ' ',
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
			INSERT INTO [dbo].[locations]
           ([name]
           ,[organization]
           ,[phone]
           ,[notes]
           ,[address]
           ,[active]
           ,[postcode]
		   ,[url]
		   ,[tags]
		   ,[external_key])
     VALUES
           (@name
           ,@organization
           ,@phone
           ,@notes 
           ,@address
           ,@active
           ,@postcode
		   ,@url
		   ,@tags
		   ,@external_key)

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