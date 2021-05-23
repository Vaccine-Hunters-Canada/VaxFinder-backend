-- =============================================
-- Author:      Evan Gamble
-- Create Date: 2021-05-04
-- Description: From https://www.c-sharpcorner.com/UploadFile/afenster/how-to-find-a-doctor-near-your-home-in-sql-server/
-- =============================================
CREATE FUNCTION [dbo].[CalculateDistance]  
(  
    @lat1Degrees decimal(10,6),  
    @lon1Degrees decimal(10,6),  
   
    @lat2Degrees decimal(10,6),  
    @lon2Degrees decimal(10,6)  
)  
RETURNS decimal(9,4)  
AS  
BEGIN  
   
    DECLARE @earthSphereRadiusKilometers as decimal(10,6)  
    DECLARE @kilometerConversionToMilesFactor as decimal(7,6)  
    SELECT @earthSphereRadiusKilometers = 6366.707019  
    SELECT @kilometerConversionToMilesFactor = .621371  
   
    -- convert degrees to radians  
    DECLARE @lat1Radians decimal(10,6)  
    DECLARE @lon1Radians decimal(10,6)  
    DECLARE @lat2Radians decimal(10,6)  
    DECLARE @lon2Radians decimal(10,6)  
    SELECT @lat1Radians = (@lat1Degrees / 180) * PI()  
    SELECT @lon1Radians = (@lon1Degrees / 180) * PI()  
    SELECT @lat2Radians = (@lat2Degrees / 180) * PI()  
    SELECT @lon2Radians = (@lon2Degrees / 180) * PI()  
   
    -- formula for distance from [lat1,lon1] to [lat2,lon2]  
    RETURN ROUND(2 * ASIN(SQRT(POWER(SIN((@lat1Radians - @lat2Radians) / 2) ,2)  
        + COS(@lat1Radians) * COS(@lat2Radians) * POWER(SIN((@lon1Radians - @lon2Radians) / 2), 2)))  
        * (@earthSphereRadiusKilometers * @kilometerConversionToMilesFactor), 4)  
   
END  