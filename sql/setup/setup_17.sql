
-- =============================================
-- Author:      Evan Gamble	
-- Create Date: 05-03-2021
-- Description: Calculating a geohash based on lat/long
-- =============================================
CREATE FUNCTION GetGeoHash
(
    -- Add the parameters for the function here
   @latitude decimal(10,6),
   @longitude decimal(10,6)
)
RETURNS geography
AS
BEGIN
    declare @geographyPoint geography;

	select @geographyPoint = geography::Point(@latitude, @longitude, '4326');		

	return @geographyPoint
END