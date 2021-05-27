ALTER TABLE [dbo].[locations]  WITH CHECK ADD  CONSTRAINT [FK__locations__organ__797309D9] FOREIGN KEY([organization])
REFERENCES [dbo].[organizations] ([id])