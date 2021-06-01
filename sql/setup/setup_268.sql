
CREATE TABLE [dbo].[Security](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[userName] [nchar](255) NOT NULL,
	[password] [nchar](255) NOT NULL,
	[key] [uniqueidentifier] NULL,
	[created_at] [datetime] NOT NULL
) ON [PRIMARY]