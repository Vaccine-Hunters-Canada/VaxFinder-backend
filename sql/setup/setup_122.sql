ALTER TABLE [dbo].[locations]  WITH CHECK ADD  CONSTRAINT [FK__locations__organ__656C112C] FOREIGN KEY([organization])
REFERENCES [dbo].[organizations] ([id])