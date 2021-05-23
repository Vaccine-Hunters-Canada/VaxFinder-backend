ALTER TABLE [dbo].[vaccine_availability]  WITH CHECK ADD  CONSTRAINT [FK__entries__locatio__7B5B524B] FOREIGN KEY([location])
REFERENCES [dbo].[locations] ([id])