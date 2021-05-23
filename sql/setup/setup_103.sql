/****** Object:  Index [idx_location_organization]    Script Date: 5/22/2021 5:46:18 PM ******/
CREATE NONCLUSTERED INDEX [idx_location_organization] ON [dbo].[locations]
(
	[organization] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, DROP_EXISTING = OFF, ONLINE = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]