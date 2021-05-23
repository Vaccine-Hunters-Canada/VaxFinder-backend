ALTER TABLE [dbo].[organization_keys]  WITH CHECK ADD  CONSTRAINT [FK__organizat__organ__40C49C62] FOREIGN KEY([organization])
REFERENCES [dbo].[organizations] ([id])