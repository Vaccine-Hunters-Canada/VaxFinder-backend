CREATE TABLE [dbo].[vaccine_availability](
	[id] [uniqueidentifier] NOT NULL,
	[numberAvailable] [int] NOT NULL,
	[numberTotal] [int] NULL,
	[date] [datetime] NOT NULL,
	[location] [int] NOT NULL,
	[vaccine] [int] NULL,
	[inputType] [int] NOT NULL,
	[tags] [text] NULL,
	[created_at] [datetime] NOT NULL,
 CONSTRAINT [PK__entries__3213E83F89BAFED2] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]