


CREATE procedure [dbo].[vaccine_availability_Create_Key] 
(
	@numberAvailable int
    ,@numberTotal int = null
    ,@date datetime
    ,@location int
    ,@vaccine int
    ,@inputType int
    ,@tags text = null
	,@auth uniqueidentifier   
)
AS
	SET NOCOUNT ON;
	declare @ID uniqueidentifier = newid()

	BEGIN TRY

		declare @valid bit

		select @valid = dbo.ValidateLocationKey(@auth, @location)

		if @valid = 0
		BEGIN
			return(0);
		END

		BEGIN TRANSACTION;		

			INSERT INTO [dbo].[vaccine_availability]
           ([id]
		   ,[numberAvailable]
           ,[numberTotal]
           ,[date]
           ,[location]
           ,[vaccine]
           ,[inputType]
           ,[tags])
     VALUES
           (@ID
		   ,@numberAvailable
           ,@numberTotal
           ,@date
           ,@location
           ,@vaccine
           ,@inputType
           ,@tags)

		Select @ID

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH