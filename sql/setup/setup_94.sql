CREATE TABLE [dbo].[vaccine_availability_requirements](
	[id] [uniqueidentifier] NOT NULL,
	[vaccine_availability] [uniqueidentifier] NOT NULL,
	[requirement] [int] NOT NULL,
	[active] [bit] NOT NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__entry_re__3213E83F21B23394] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]