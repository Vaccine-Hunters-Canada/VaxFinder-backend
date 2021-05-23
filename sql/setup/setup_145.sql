

CREATE procedure [dbo].[address_Update] 
(
	@addressID int,
	@line1 varchar(255),
    @line2 varchar(255),
    @city varchar(255),
    @province nvarchar(255),
    @postcode varchar(6),
	@latitude decimal(10,6) = null,
	@longitude decimal(10,6) = null,
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

		
		DECLARE @geographyPoint geography

		if (@latitude is not null)
		begin
			if (@longitude is not null)
			begin
				select @geographyPoint = geography::Point(@latitude, @longitude, '4326');
					
				update dbo.[address] set line1=@line1, line2 = @line2, city = @city, province = @province, postcode = @postcode, [location] = @geographyPoint 
				where id = @addressID

				return(@addressID);
			end
			else
			begin
				update dbo.[address] set line1=@line1, line2 = @line2, city = @city, province = @province, postcode = @postcode
				where id = @addressID

				return(@addressID);
			end			
		end

		update dbo.[address] set line1=@line1, line2 = @line2, city = @city, province = @province, postcode = @postcode
		where id = @addressID		
		
		RETURN(@addressID);

	END TRY

	BEGIN CATCH



		RETURN(-1);

	END CATCH