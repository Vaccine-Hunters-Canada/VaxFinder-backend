

CREATE procedure [dbo].[locations_ReadByExternalKey] 
(
	@external_key varchar(255)
)
AS
	SET NOCOUNT ON;

	

		
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
		
		RETURN(1);