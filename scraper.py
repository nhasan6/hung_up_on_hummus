from playwright.sync_api import expect, sync_playwright
import time
from send_alert import send_email

def detect_deal(page):
    # look for BOGO deal
    deal_popup = page.get_by_role("dialog").filter(has_text="Buy 1, Get 1").or_(page.get_by_role("dialog").filter(has_text="PROMO CODE"))
    if (deal_popup.count() > 0):
        body = deal_popup.text_content()
        subject = "EAST TEA CAN LEGENDARY HUMMUS + CHICKEN BOGO! ON NOW!"
        send_email(subject, body) 
    else:
        # alternatively, check if price has decreased
        menu_item = page.get_by_role("listitem").filter(has=page.get_by_role("heading", name ="Legendary Hummus + Chicken")).get_by_test_id("price-2c74bb69-ea49-4faf-99c9-e0fc70f86bcc")
        price = menu_item.text_content().strip()[1:] # remove dollar sign ($15.75)
        if (float(price) < 15.75):
            subject = "EAST TEA CAN LEGENDARY HUMMUS + CHICKEN PRICE DROP!"
            body = f"The online ordering price is currently ${price}!"
            send_email(subject, body)
        else:
            print("no deal")

try:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto("https://order.toasttab.com/online/east-tea-can-new-3115-winston-churchill-blvd-unit-1")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        expect(page.locator("h2").nth(0)).to_contain_text("East Tea Can Mississauga") # checks that we're seeing expected info
        print(page.locator("h2").nth(0).text_content())

        detect_deal(page)
        browser.close()    

except Exception as err:
        subject = "Hummus Bot Error"
        send_email(subject, str(err))
