
ALTER TABLE [dbo].[Security] ADD  CONSTRAINT [DF_Security_created_at]  DEFAULT (getdate()) FOR [created_at]