-- =============================================
-- Author:		Evan Gamble
-- Create date: 2021-04-05
-- Description:	Function call
-- =============================================
CREATE FUNCTION [dbo].[udfGetPostCodesNearMe] (
    @Latitude DECIMAL(10,6),  
    @Longitude DECIMAL(10,6),
	@LatRad DECIMAL(2,2),
	@LonRad DECIMAL(2,2)
)
RETURNS TABLE
AS
RETURN     
    select distinct  
    PC.postal    
    from dbo.postal_geo PC
    where (ABS(@Latitude - PC.Lat) < @LatRad)  -- Lines of latitude are ~69 miles apart.   
    and (ABS(@Longitude - PC.Lon) < @LonRad)  -- Lines of longitude in the U.S. are ~53 miles apart.            
	