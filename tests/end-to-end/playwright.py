# --------
# Another examples to test using pytest-playwright
# --------


def test_login(page: Page):
    # launch browserstack demo
    page.goto("https://bstackdemo.com/")
    # click on sign button
    page.click("#signin")
    # select Username
    page.get_by_text("Select Username").click()
    page.locator("#react-select-2-option-0-0").click()
    # select Password
    page.get_by_text("Select Password").click()
    page.locator("#react-select-3-option-0-0").click()
    # click login
    page.get_by_role("button", name="Log In").click()
    # verify user have logged in
    assert page.get_by_text("demouser").is_visible()


def test_item_purchase(page: Page):
    page.goto("https://bstackdemo.com/")
    # add to cart
    page.locator('[id="\\35 "]').get_by_text("Add to cart").click()
    # checkout
    page.get_by_text("Checkout").click()
    # login
    page.type("#react-select-2-input", "demouser\n")
    page.type("#react-select-3-input", "testingisfun99\n")
    page.get_by_role("button", name="Log In").click()
    # fill shipping address
    page.get_by_label("First Name").fill("Test")
    page.get_by_label("Last Name").fill("Test")
    page.get_by_label("Address").fill("Test address")
    page.get_by_label("State/Province").fill("Test State")
    page.get_by_label("Postal Code").fill("123456")
    # click submit
    page.locator("#checkout-shipping-continue").click()
    # verify success message
    page.wait_for_timeout(1000)
    assert page.locator("#confirmation-message").is_visible()
