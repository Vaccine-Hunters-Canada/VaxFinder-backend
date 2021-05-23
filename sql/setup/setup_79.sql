CREATE TABLE [dbo].[organizations](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[full_name] [varchar](255) NULL,
	[short_name] [varchar](50) NULL,
	[description] [varchar](2000) NULL,
	[url] [varchar](255) NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__organiza__3213E83FB21EF2A6] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]