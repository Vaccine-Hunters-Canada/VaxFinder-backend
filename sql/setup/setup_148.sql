-- =============================================
-- Author:      Evan Gamble
-- Create Date: 04-30-2021
-- Description: Get all avaliable vaccines
-- =============================================
CREATE PROCEDURE [dbo].[GetAvailableVaccines]
(
    @postal varchar(6),
    @date datetime
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

        BEGIN TRY
            declare @lat decimal (10,6)
            declare @lon decimal (10,6)
            declare @radLat decimal (2,2)
            declare @radLon decimal (2,2)

            select @lat= postal_geo.lat, @lon = postal_geo.lon from dbo.postal_geo where postal_geo.postal = left(@postal,3)			

            set @radLat = 0.5
            set @radLon = 0.5
			
			select va.id, va.numberAvailable, va.numberTotal, va.[date], va.[location], va.[vaccine], va.[inputType], va.[tags], va.[created_at],  IDENTITY(INT, 1, 1) as [sort] into #vaccine_availability_temp 
			from dbo.vaccine_availability va join dbo.locations on va.[location] = locations.id
			where left([locations].postcode,3) in ( select PC.postal from dbo.postal_geo PC where (ABS(@lat - PC.Lat) < @radLat) and (ABS(@lon - PC.Lon) < @radLon) ) and  [date] > @date 
			order by [location], [date]


			select [location], [date], max(created_at) as [created_at] into #filter from #vaccine_availability_temp  group by [location], [date]
			
			--delete from #vaccine_availability_temp where id not in (select id from #filter f join #vaccine_availability_temp va on va.created_at = f.created_at AND va.location = f.location)

            -- vaccine_availability table
            SELECT va.id, va.numberAvailable, va.numberTotal, va.[date], va.[location], va.[vaccine], va.[inputType], va.[tags], va.[created_at] from #vaccine_availability_temp VA
            join 
                locations
                on [location] = [locations].id                       
			order by
				sort            

			select dbo.vaccine_availability_timeslots.* from dbo.vaccine_availability_timeslots join #vaccine_availability_temp on #vaccine_availability_temp.id = vaccine_availability_timeslots.vaccine_availability
			order by
				sort
            
			
			 SELECT vars.*, reqs.name, reqs.description
			 FROM dbo.vaccine_availability_requirements vars
			 JOIN dbo.requirements reqs on vars.requirement = reqs.id 
				join #vaccine_availability_temp on #vaccine_availability_temp.id = vars.vaccine_availability
			order by
				sort
            
			select dbo.locations.* from dbo.locations join #vaccine_availability_temp on  #vaccine_availability_temp.[location] = locations.id
			order by
				sort
            
			select dbo.address.id, dbo.address.line1, dbo.address.line2, dbo.address.city, dbo.address.province, dbo.address.postcode, dbo.address.created_at from dbo.locations join #vaccine_availability_temp on #vaccine_availability_temp.[location] = locations.id join [address] on address.id = locations.[address]
			order by 
				sort            
			
			SELECT dbo.organizations.* from dbo.organizations join dbo.locations on locations.organization = organizations.id join #vaccine_availability_temp va on va.location = locations.id
			order by 
				sort    

			drop table #vaccine_availability_temp
			drop table #filter
        END TRY
        BEGIN CATCH

--          

            RETURN(-1);

        END CATCH
END