
class AlertHandler:

    @staticmethod
    async def open_alert(page, alert):
        page.dialog = alert
        alert.open = True
        await page.update_async()

    @staticmethod
    async def close_alert(e, page, alert):
        alert.open = False
        await page.update_async()
        page.dialog = None


