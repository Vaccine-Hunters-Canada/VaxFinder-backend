
-- =============================================
-- Author:      Evan Gamble
-- Create Date: 2021-05-04
-- Description: From https://www.c-sharpcorner.com/UploadFile/afenster/how-to-find-a-doctor-near-your-home-in-sql-server/
-- =============================================
CREATE PROCEDURE [dbo].[PostalCodesNearLatLongAndRad]  
   
            @Latitude DECIMAL(10,6),  
            @Longitude DECIMAL(10,6),
			@LatRad DECIMAL(2,2),
			@LonRad DECIMAL(2,2)
AS  
BEGIN  
            SET NOCOUNT ON;  
            select distinct  
            PC.postal,
            PC.lat,
            PC.lon,
            dbo.CalculateDistance(@Latitude, @Longitude, PC.Lat, PC.Lon) as Distance            
            from dbo.postal_geo PC
            where (ABS(@Latitude - PC.Lat) < @LatRad)  -- Lines of latitude are ~69 miles apart.   
            and (ABS(@Longitude - PC.Lon) < @LonRad)  -- Lines of longitude in the U.S. are ~53 miles apart.            
			order by Distance
END