ALTER TABLE [dbo].[vaccines] ADD  CONSTRAINT [DF_vaccines_created_at]  DEFAULT (getdate()) FOR [created_at]