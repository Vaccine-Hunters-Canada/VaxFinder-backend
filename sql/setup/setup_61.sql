CREATE TABLE [dbo].[address](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[line1] [varchar](255) NULL,
	[line2] [varchar](255) NULL,
	[city] [varchar](255) NULL,
	[province] [nvarchar](255) NOT NULL,
	[postcode] [varchar](6) NOT NULL,
	[location] [geography] NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__address__3213E83FCFA7B88B] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]