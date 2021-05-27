CREATE TABLE [dbo].[keys](
	[id] [uniqueidentifier] NOT NULL,
	[start_date] [datetime] NOT NULL,
	[end_date] [datetime] NOT NULL,
	[role] [nvarchar](255) NOT NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__keys__3213E83F54969EF5] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]