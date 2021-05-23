/****** Object:  Index [idx_va_t]    Script Date: 5/22/2021 5:46:18 PM ******/
CREATE NONCLUSTERED INDEX [idx_va_t] ON [dbo].[vaccine_availability_timeslots]
(
	[vaccine_availability] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, DROP_EXISTING = OFF, ONLINE = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]