
CREATE procedure [dbo].[address_Read] 
(
	@addressID int
)
AS
			select id, line1, line2, city, province, postcode, created_at from address where id = @addressID

	
		
		RETURN(@addressID);
