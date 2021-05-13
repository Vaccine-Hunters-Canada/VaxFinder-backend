
CREATE PROCEDURE [dbo].[GetVaccineLocationsNearby]
(
    @postal varchar(6),
    @date datetime
)
AS
BEGIN
    -- SET NOCOUNT ON is added to prevent extra result sets from interfering with SELECT statements.
    SET NOCOUNT ON
        BEGIN TRY
            DECLARE @lat decimal (10,6)
            DECLARE @lon decimal (10,6)
            DECLARE @radLat decimal (2,2)
            DECLARE @radLon decimal (2,2)

            SELECT @lat= postal_geo.lat, @lon = postal_geo.lon
            FROM dbo.postal_geo
            WHERE postal_geo.postal = left(@postal,3)

            SET @radLat = 0.5
            SET @radLon = 0.5

            -- Store locations near a postal code into a temporary table
            SELECT *
            INTO #locations_temp
            FROM dbo.locations l
            WHERE left(l.postcode, 3) IN (
                SELECT pc.postal FROM dbo.postal_geo pc
                WHERE (ABS(@lat - pc.Lat) < @radLat) AND (ABS(@lon - pc.Lon) < @radLon)
            )

            -- Select locations near a postal code
            SELECT * FROM #locations_temp

            -- Select organizations at locations near a postal code
            SELECT o.*
            FROM dbo.organizations o
            JOIN #locations_temp lt
                ON o.id = lt.organization

            -- Select addresses at locations near a postal code
            SELECT a.id, a.line1, a.line2, a.city, a.province, a.postcode, a.created_at
            FROM dbo.address a
            JOIN #locations_temp lt
                ON a.id = lt.address

            -- Store vaccine availabilities for locations near a postal code (and after @date) into a temporary table
            SELECT va.*,  IDENTITY(INT, 1, 1) as [selected_vaccine_availabilities]
            INTO #vaccine_availability_temp
            FROM dbo.vaccine_availability va
            JOIN #locations_temp
                ON #locations_temp.id = va.location AND va.date > @date
            ORDER BY va.date

            -- Select vaccine availabilities for locations near a postal code (and after @date)
            SELECT
                   vat.id,
                   vat.numberAvailable,
                   vat.numberTotal,
                   vat.date,
                   vat.location,
                   vat.vaccine,
                   vat.inputType,
                   vat.tags,
                   vat.created_at
            FROM #vaccine_availability_temp vat

            -- Select children (timeslots) for vaccine availabilities for locations near a postal code (and after @date)
            SELECT vac.*
            FROM dbo.vaccine_availability_children vac
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vac.vaccine_availability
            ORDER BY selected_vaccine_availabilities, vac.taken_at DESC, vac.time

            --- Select requirements for vaccine availabilities for locations near a postal code (and after @date)
            SELECT vars.*
            FROM dbo.vaccine_availability_requirements vars
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vars.vaccine_availability
            ORDER BY selected_vaccine_availabilities

            -- Drop temporary tables
            DROP TABLE #vaccine_availability_temp
            DROP TABLE #locations_temp
        END TRY
        BEGIN CATCH
            -- Rollback transaction
            IF XACT_STATE() <> 0
                ROLLBACK TRANSACTION;
            RETURN(-1);
        END CATCH
END