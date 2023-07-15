from playwright.sync_api import Playwright, expect


def test_register_login(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/")

    # register
    page.get_by_role("link", name="Register!").click()
    page.screenshot(path="screenshots/register_form.png", full_page=True)
    page.locator('input[name="email"]').fill("test007@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    page.locator('input[name="confirm_password"]').fill("qwerty")
    page.get_by_role("button", name="Register").click()

    # login
    page.screenshot(path="screenshots/login_form.png", full_page=True)
    page.locator('input[name="email"]').fill("test44@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    page.get_by_role("button", name="Login").click()

    # Assert index page
    expect(page.locator("p")).to_contain_text(["You haven't added any movies yet"])
    page.get_by_role("link", name="Add one!").click()
