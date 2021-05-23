CREATE TABLE [dbo].[vaccines](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](50) NOT NULL,
	[description] [varchar](255) NOT NULL,
	[code] [varchar](2) NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__vaccines__3213E83F858FCB46] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]