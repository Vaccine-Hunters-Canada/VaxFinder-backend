
CREATE procedure [dbo].[locations_Read] 
(
	@locationID int = null,
	@organizationID int = null,
	@external_key varchar(255) = null
)
AS
	SET NOCOUNT ON;
	declare @ID int = 0;
	BEGIN TRY

			if (@locationID is not null)
			BEGIN
				select [id]
				  ,[name]
				  ,[organization]
				  ,[phone]
				  ,[notes]
				  ,[address]
				  ,[active]
				  ,[postcode]
				  ,[url]
				  ,[tags] 
				  ,[created_at]	
				  from locations where id = @locationID

				  return(@locationID)
			END			

			if (@external_key is not null)
			BEGIN
				select [id]
				  ,[name]
				  ,[organization]
				  ,[phone]
				  ,[notes]
				  ,[address]
				  ,[active]
				  ,[postcode]
				  ,[url]
				  ,[tags] 
				  ,[created_at]	
				  from locations where external_key = @external_key

				  return(1)
			END

			if (@organizationID is not null)
			BEGIN
				select [id]
				  ,[name]
				  ,[organization]
				  ,[phone]
				  ,[notes]
				  ,[address]
				  ,[active]
				  ,[postcode]
				  ,[url]
				  ,[tags] 
				  ,[created_at]	
				  from locations where organization = @organizationID

				  return(1)
			END

		select [id]
			,[name]
			,[organization]
			,[phone]
			,[notes]
			,[address]
			,[active]
			,[postcode]
			,[url]
			,[tags] 
			,[created_at]	
		from locations

	END TRY

	BEGIN CATCH


		RETURN(-1);

	END CATCH