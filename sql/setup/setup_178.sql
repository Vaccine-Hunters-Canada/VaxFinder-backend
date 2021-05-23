

CREATE procedure [dbo].[locations_ReadByOrganization] 
(
	@organizationID int
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
				  from locations where organization = @organizationID

		
		
		RETURN(1);

	