CREATE PROCEDURE [dbo].[GetVaccineLocationsNearby]
(
    @postal varchar(6),
    @date datetime,
	@includeEmpty bit
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

            SET @radLat = 0.25
            SET @radLon = 0.25

            -- Store locations near a postal code into a temporary table
            SELECT l.*, dbo.CalculateDistance(@lat,@lon,p.lat,p.lon) as distance
            INTO #locations_temp
            FROM dbo.locations l join
				 dbo.postal_geo p on p.postal = left(l.postcode,3)
            WHERE left(l.postcode, 3) IN (
                SELECT pc.postal FROM dbo.postal_geo pc
                WHERE (ABS(@lat - pc.Lat) < @radLat) AND (ABS(@lon - pc.Lon) < @radLon)
            )

            -- Store vaccine availabilities for locations near a postal code (and after @date) into a temporary table
            SELECT va.*,  IDENTITY(INT, 1, 1) as [selected_vaccine_availabilities]
            INTO #vaccine_availability_temp
            FROM dbo.vaccine_availability va
            JOIN #locations_temp
                ON #locations_temp.id = va.location AND va.date >= @date
            ORDER BY va.date

			--Remove empty availabilities from list
			if @includeEmpty = 0
			BEGIN
				delete from #vaccine_availability_temp where numberAvailable < 1

				delete from #locations_temp where id not in (select location from #vaccine_availability_temp)
			END

			-- Select locations near a postal code
            SELECT * FROM #locations_temp order by distance

            -- Select organizations at locations near a postal code
            SELECT o.*
            FROM dbo.organizations o
            JOIN #locations_temp lt
                ON o.id = lt.organization
			order by distance

            -- Select addresses at locations near a postal code
            SELECT a.id, a.line1, a.line2, a.city, a.province, a.postcode, a.created_at
            FROM dbo.address a
            JOIN #locations_temp lt
                ON a.id = lt.address
			order by distance

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
            SELECT vat.*
            FROM dbo.vaccine_availability_timeslots vat
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vat.vaccine_availability
            ORDER BY selected_vaccine_availabilities, vat.taken_at DESC, vat.time

            --- Select requirements for vaccine availabilities for locations near a postal code (and after @date)
            SELECT vars.*, reqs.name, reqs.description
            FROM dbo.vaccine_availability_requirements vars
            JOIN #vaccine_availability_temp
                ON #vaccine_availability_temp.id = vars.vaccine_availability
			JOIN dbo.requirements reqs on vars.requirement = reqs.id
            ORDER BY selected_vaccine_availabilities

            -- Drop temporary tables
            DROP TABLE #vaccine_availability_temp
            DROP TABLE #locations_temp
        END TRY
        BEGIN CATCH
           
            RETURN(-1);
        END CATCH
END