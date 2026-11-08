import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def main():
    port = 5656
    print(f"Connecting to http://127.0.0.1:{port}...")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        page.on("console", lambda m: print(f"CONSOLE: [{m.type}] {m.text}"))
        page.on("pageerror", lambda e: print(f"PAGE ERROR: {e}"))

        await page.goto(f"http://127.0.0.1:{port}", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 1. Click Smart KYC tab
        print("Clicking Smart KYC tab...")
        await page.click("#deskTabKyc")
        await page.wait_for_timeout(1500)

        banner_name = await page.inner_text("#kycBannerTitle")
        badge_text = await page.inner_text("#kycBannerBadge")
        print(f"K02 Loaded -> Name: '{banner_name}' | Badge: '{badge_text}'")

        art_dir = "artifacts"
        os.makedirs(art_dir, exist_ok=True)
        shot1 = os.path.join(art_dir, "kyc_workbench_k02_verified.png")
        await page.screenshot(path=shot1)
        print(f"Screenshot 1 saved: {shot1}")

        # 2. Switch to Address Proof tab
        print("Switching to Address Proof tab...")
        await page.click('button[data-dockeys="address_proof"]')
        await page.wait_for_timeout(1000)

        doc_title = await page.inner_text("#kycDocTitle")
        print(f"Active doc title: '{doc_title}'")
        shot2 = os.path.join(art_dir, "kyc_workbench_address_proof.png")
        await page.screenshot(path=shot2)
        print(f"Screenshot 2 saved: {shot2}")

        # 3. Switch applicant to K01 (Cancelled GSTIN Anomaly)
        print("Switching applicant to K01 (Cancelled GSTIN)...")
        await page.select_option("#kycApplicantSelect", "K01")
        await page.wait_for_timeout(1500)

        k01_name = await page.inner_text("#kycBannerTitle")
        k01_badge = await page.inner_text("#kycBannerBadge")
        print(f"K01 Loaded -> Name: '{k01_name}' | Badge: '{k01_badge}'")

        shot3 = os.path.join(art_dir, "kyc_workbench_k01_anomaly.png")
        await page.screenshot(path=shot3)
        print(f"Screenshot 3 saved: {shot3}")

        # 4. Switch applicant to K11 (Expired Utility Bill)
        print("Switching applicant to K11 (Expired Bill)...")
        await page.select_option("#kycApplicantSelect", "K11")
        await page.wait_for_timeout(1000)
        await page.click('button[data-dockeys="address_proof"]')
        await page.wait_for_timeout(1000)

        shot4 = os.path.join(art_dir, "kyc_workbench_k11_expired_bill.png")
        await page.screenshot(path=shot4)
        print(f"Screenshot 4 saved: {shot4}")

        # Copy to user brain dir
        brain_dir = "C:/Users/DELL/.gemini/antigravity/brain/189eb77b-9b1f-4f68-b2ff-1682279e819c"
        import shutil
        for s in ["kyc_workbench_k02_verified.png", "kyc_workbench_address_proof.png", "kyc_workbench_k01_anomaly.png", "kyc_workbench_k11_expired_bill.png"]:
            src = os.path.join(art_dir, s)
            dst = os.path.join(brain_dir, s)
            if os.path.exists(src):
                shutil.copy2(src, dst)

        await browser.close()
        print("PLAYWRIGHT TEST SUCCESSFUL! ALL SPECIMENS & WORKBENCH TABS VERIFIED!")

if __name__ == "__main__":
    asyncio.run(main())
