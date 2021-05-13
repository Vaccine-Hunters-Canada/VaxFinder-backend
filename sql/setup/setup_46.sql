
-- =============================================
-- Author:      Alvin
-- =============================================
CREATE PROCEDURE dbo.testingstuff
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

	select id from dbo.address
	select id from dbo.vaccine_availability

	return(-1)
END