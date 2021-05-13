
CREATE FUNCTION dbo.ValidateKey(@key uniqueidentifier, @location int)
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

	IF @role = 3
	BEGIN
		declare @count int
		set @count = 0

		select @count = count(*) from dbo.location_keys where [location] = @location and [key] = @key

		if @count > 0
		BEGIN
			return 1
		END

	END

	return 0
END