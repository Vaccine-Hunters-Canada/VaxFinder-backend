ALTER TABLE [dbo].[vaccine_availability]  WITH CHECK ADD  CONSTRAINT [FK__entries__vaccine__7C4F7684] FOREIGN KEY([vaccine])
REFERENCES [dbo].[vaccines] ([id])