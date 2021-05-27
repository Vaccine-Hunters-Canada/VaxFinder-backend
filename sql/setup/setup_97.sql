CREATE TABLE [dbo].[vaccine_availability_timeslots](
	[id] [uniqueidentifier] NOT NULL,
	[vaccine_availability] [uniqueidentifier] NOT NULL,
	[time] [datetime] NOT NULL,
	[taken_at] [datetime] NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__entry_ch__3213E83F364F5FA4] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]