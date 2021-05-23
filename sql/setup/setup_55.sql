CREATE TABLE [dbo].[postal_geo](
	[postal] [nchar](3) NOT NULL,
	[area] [nchar](255) NOT NULL,
	[province] [nchar](255) NOT NULL,
	[lat] [decimal](10, 6) NOT NULL,
	[lon] [decimal](10, 6) NOT NULL,
	[geohash] [geography] NULL,
 CONSTRAINT [PK_postal_geo] PRIMARY KEY CLUSTERED 
(
	[postal] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]