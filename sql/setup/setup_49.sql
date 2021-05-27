CREATE FUNCTION [dbo].[ValidateLocationKey](@key uniqueidentifier, @location int)
RETURNS bit AS
BEGIN
    declare @role int
	select @role = [role] from dbo.keys where id = @key

	IF @role = 1
	BEGIN
		RETURN 1
	END
    
	IF @role = 2
	BEGIN
		RETURN 1
	END

	declare @count int

	IF @role = 3
	BEGIN
		
		set @count = 0		
		

		select @count = count(*) from dbo.location_keys where [location] = @location and [key] = @key

		if @count > 0
		BEGIN
			return 1
		END

	END

	if @role = 4
	BEGIN
		declare @organization int
		select @organization = organization from dbo.locations
				
		set @count = 0		

		select @count = count(*) from dbo.organization_keys where [organization] = @organization and [key] = @key

		if @count > 0
		BEGIN
			return 1
		END
	END

	return 0
END