/****** Object:  Index [idx_va_r]    Script Date: 5/22/2021 5:46:18 PM ******/
CREATE NONCLUSTERED INDEX [idx_va_r] ON [dbo].[vaccine_availability_requirements]
(
	[vaccine_availability] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, DROP_EXISTING = OFF, ONLINE = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]