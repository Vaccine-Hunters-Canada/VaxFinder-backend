CREATE TABLE [dbo].[requirements](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](255) NOT NULL,
	[description] [varchar](255) NOT NULL,
	[created_at] [datetime] NOT NULL,
	[requirementGroup] [varchar](255) NULL,
 CONSTRAINT [PK__requirem__3213E83F3CCDBD82] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]