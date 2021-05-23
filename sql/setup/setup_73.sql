CREATE TABLE [dbo].[locations](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](255) NOT NULL,
	[organization] [int] NULL,
	[phone] [varchar](255) NULL,
	[notes] [text] NULL,
	[address] [int] NULL,
	[active] [bit] NOT NULL,
	[postcode] [varchar](6) NULL,
	[url] [varchar](255) NULL,
	[tags] [text] NULL,
	[created_at] [datetime] NOT NULL,
	[external_key] [nvarchar](255) NULL,
 CONSTRAINT [PK__location__3213E83F9A5A87D6] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]