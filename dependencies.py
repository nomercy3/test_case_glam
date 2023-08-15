# Imports
from enum import Enum
from pydantic import BaseModel
from playwright.async_api import async_playwright, TimeoutError, Page
from playwright_stealth import stealth_async
from fastapi import HTTPException
from starlette import status


class ImageUrlsResponseDTO(BaseModel):
    urls: list[str]


class APITags(Enum):
    INSTAGRAM = 'Instagram'


class NotFoundHTTPException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InstagramParserService:

    async def parse(self, username: str, max_count: int) -> list[str]:
        urls = []

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)

            page = await browser.new_page()
            await page.goto(f'https://instagram.com/{username}/')

            try:

                # apply stealth
                await stealth_async(page)

                # click on decline cookies warning
                await page.click('button._a9--._a9_1')

                # wait for the loading
                await page.wait_for_load_state('networkidle')

                # scroll down until required number of photos are in DOM
                photos: list = await page.query_selector_all('div._aagv')
                while len(photos) < max_count:
                    await page.keyboard.press('End')
                    await self._handle_login_modal_(page)

                # save only required number of photos
                urls = [item.get_attribute('src') for item in photos[:max_count]]

            except TimeoutError:
                raise ValueError

        return urls

    # PRIVATE METHODS

    @staticmethod
    async def _handle_login_modal_(page: Page):
        selector = '#mount_0_0_DF > div > div > div:nth-child(3) > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._ab9z._aba9._abch._abck.x1vjfegm._abcm > div'
        login_modal = page.locator(selector)
        if await login_modal.is_visible():
            await login_modal.click()
