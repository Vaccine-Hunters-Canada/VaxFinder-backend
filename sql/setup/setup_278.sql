


CREATE procedure [dbo].[security_Login] 
(
	@userName varchar(255),
	@password varchar(255)
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY
			
			DECLARE @ret int

			set @ret = 0;


			select @ret = COUNT(*) from dbo.[security] where trim(userName) = trim(@userName) and trim([password]) = trim(@password)

			if (@ret > 0)
			BEGIN
				select * from dbo.[security] where trim(userName) = trim(@userName) and trim([password]) = trim(@password)

				return @ret
			END

			return @ret

	END TRY

	BEGIN CATCH

		RETURN(-1);

	END CATCH