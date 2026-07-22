#!/usr/bin/env python3
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML = Path("/home/ubuntu/.openclaw/workspace-health/reports/MDT-2026-07-22.html")
PDF  = Path("/home/ubuntu/.openclaw/workspace-health/reports/MDT-2026-07-22.pdf")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{HTML.resolve()}")
        await page.emulate_media(media="print")
        await page.pdf(
            path=str(PDF),
            format="A4",
            margin={"top":"18mm","bottom":"18mm","left":"16mm","right":"16mm"},
            print_background=True,
        )
        await browser.close()
    print(f"[ok] {PDF}")

asyncio.run(main())
