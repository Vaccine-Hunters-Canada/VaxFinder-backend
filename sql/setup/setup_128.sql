ALTER TABLE [dbo].[organization_keys]  WITH CHECK ADD  CONSTRAINT [FK__organizatio__key__41B8C09B] FOREIGN KEY([key])
REFERENCES [dbo].[keys] ([id])