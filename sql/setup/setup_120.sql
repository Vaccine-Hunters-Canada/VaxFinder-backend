ALTER TABLE [dbo].[locations]  WITH CHECK ADD  CONSTRAINT [FK__locations__addre__7A672E12] FOREIGN KEY([address])
REFERENCES [dbo].[address] ([id])