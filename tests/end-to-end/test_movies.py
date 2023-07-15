from flask import url_for
from playwright.sync_api import Playwright, Page, expect

# --------------
# PLAYWRIGHT TESTS
# --------------


def test_take_screenshot(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/")

    page.screenshot(path="screenshots/home.png", full_page=True)


# def test_homepage_loads(live_server, page: Page):
#     page.goto(url_for("movie.home", _external=True))
#     expect(page.locator("h1")).to_contain_text(["Welcome to the"])


def test_login_add_movie(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/auth/login")

    # Login
    page.locator('input[name="email"]').fill("test3@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    expect(page.locator(".button--form")).to_contain_text(["Login"])
    page.locator('input[name="password"]').press("Enter")
    # redirect to index without movies
    page.screenshot(path="screenshots/index_0.png", full_page=True)
    # Add movie
    page.get_by_role("link", name="+").click()
    page.screenshot(path="screenshots/add_form_before.png", full_page=True)
    page.locator('input[name="title"]').fill("Fast & Furious 3")
    page.locator('input[name="director"]').fill("John Doe")
    page.get_by_role("spinbutton").fill("2020")
    page.get_by_label("Cast").fill("Dominic Toretto\nBrian O'Conner\nLetty\nMia\nGisele")
    page.get_by_label("Series").fill("Fast & Furious 1\nFast 2 Furious")
    page.get_by_label("Tags").fill("Action\nThriller")
    page.get_by_label("Description").fill(
        "Brian O'Conner, back working for the FBI in Los Angeles, teams up with Dominic Toretto to bring down a heroin importer by infiltrating his operation."
    )
    page.locator('input[name="video_link"]').fill("https://www.youtube.com/embed/k98tBkRsGl4")
    expect(page.locator(".button--form")).to_contain_text(["Add Movie"])
    page.screenshot(path="screenshots/add_form_after.png", full_page=True)
    page.get_by_role("button", name="Add Movie").click()
    # redirect to index with movies that have been added
    page.screenshot(path="screenshots/index_1.png", full_page=True)


def test_login_add_and_delete_movie(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000")

    # Login
    page.get_by_role("link", name="Login!").click()
    page.locator('input[name="email"]').fill("test3@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    page.locator('input[name="password"]').press("Enter")

    # Add movie
    page.get_by_role("link", name="+").click()
    page.locator('input[name="title"]').fill("Fast & Furious 2")
    page.locator('input[name="director"]').fill("John Doe")
    page.get_by_role("spinbutton").fill("2016")
    page.get_by_label("Cast").fill("Dominic Toretto\nBrian O'Conner\nLetty\nMia\nGisele")
    page.get_by_label("Series").fill("Fast & Furious 1\nFast 2 Furious")
    page.get_by_label("Tags").fill("Action\nThriller")
    page.get_by_label("Description").fill("Brian O'Conner, back working for the FBI in Los Angeles.")
    page.locator('input[name="video_link"]').fill("https://www.youtube.com/embed/k98tBkRsGl4")
    expect(page.locator(".button--form")).to_contain_text(["Add Movie"])
    page.get_by_role("button", name="Add Movie").click()

    # delete movie
    page.screenshot(path="screenshots/delete_movie_before.png", full_page=True)
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("link", name="Delete").first.click()
    page.screenshot(path="screenshots/delete_movie_after.png", full_page=True)


def test_movie_single_page(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/")

    # Login
    page.get_by_role("link", name="Login!").click()
    page.locator('input[name="email"]').fill("test3@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    page.locator('input[name="password"]').press("Enter")
    # add movie
    page.get_by_role("link", name="+").click()
    page.locator('input[name="title"]').fill("Fast & Furious 4")
    page.locator('input[name="director"]').fill("John Doe")
    page.get_by_role("spinbutton").fill("2020")
    page.get_by_label("Cast").fill("Dominic Toretto\nBrian O'Conner\nLetty\nMia\nGisele")
    page.get_by_label("Series").fill("Fast & Furious 1\nFast 2 Furious")
    page.get_by_label("Tags").fill("Action\nThriller")
    page.locator('input[name="video_link"]').fill("https://www.youtube.com/embed/k98tBkRsGl4")
    expect(page.locator(".button--form")).to_contain_text(["Add Movie"])
    page.get_by_role("button", name="Add Movie").click()
    # single page
    page.get_by_role("row", name="Fast & Furious 2 By John Doe 2016 View Delete").get_by_role(
        "link", name="View"
    ).click()
    # add rate to the movie (5 stars)
    page.locator("a:nth-child(5)").click()
    # add watched date
    page.get_by_role("link", name="Not watched yet").click()
    # add tag
    page.get_by_role("link", name="Add").click()
    page.get_by_label("Tags").click()
    page.get_by_label("Tags").fill("Terror")
    page.screenshot(path="screenshots/add_tag_form.png", full_page=True)
    page.get_by_role("button", name="Submit").click()
    page.screenshot(path="screenshots/single_movie_tag_added.png", full_page=True)
    # delete tag
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("link", name="Terror").click()
    page.screenshot(path="screenshots/single_movie_tag_deleted.png", full_page=True)


def test_night_theme(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/")

    # Login
    page.get_by_role("link", name="Login!").click()
    page.locator('input[name="email"]').fill("test3@test.com")
    page.locator('input[name="password"]').fill("qwerty")
    page.locator('input[name="password"]').press("Enter")
    # night theme change
    page.get_by_role("navigation").get_by_role("link").nth(2).click()
    page.screenshot(path="screenshots/dark_index.png", full_page=True)
    # add movie
    page.get_by_role("link", name="+").click()
    page.screenshot(path="screenshots/dark_add_form_before.png", full_page=True)
    page.locator('input[name="title"]').fill("Fast & Furious 9")
    page.locator('input[name="director"]').fill("John Doe")
    page.get_by_role("spinbutton").fill("2020")
    page.get_by_label("Cast").fill("Dominic Toretto\nBrian O'Conner\nLetty\nMia\nGisele")
    page.get_by_label("Series").fill("Fast & Furious 1\nFast 2 Furious")
    page.get_by_label("Tags").fill("Action\nThriller")
    expect(page.locator(".button--form")).to_contain_text(["Add Movie"])
    page.get_by_role("button", name="Add Movie").click()
    # single page
    page.get_by_role("row", name="Fast & Furious 9 By John Doe 2020 View Delete").get_by_role(
        "link", name="View"
    ).click()
    page.screenshot(path="screenshots/dark_rating_before.png", full_page=True)
    page.locator("a:nth-child(4)").click()
    page.screenshot(path="screenshots/dark_rating_after.png", full_page=True)
    # watched date
    page.screenshot(path="screenshots/dark_watched_before.png", full_page=True)
    page.get_by_role("link", name="Not watched yet").click()
    page.screenshot(path="screenshots/dark_watched_after.png", full_page=True)
    # edit movie form
    page.get_by_role("link", name="Edit").click()
    page.screenshot(path="screenshots/dark_edit_before.png", full_page=True)
    page.locator('input[name="video_link"]').fill("https://www.youtube.com/embed/k98tBkRsGl4")
    page.screenshot(path="screenshots/dark_edit_after.png", full_page=True)
    page.locator('input[name="video_link"]').press("Enter")
    #  add tags
    page.get_by_role("link", name="Add", exact=True).click()
    page.screenshot(path="screenshots/dark_add_tag_before.png", full_page=True)
    page.get_by_label("Tags").fill("Emotion\nCars\nTerror")
    page.get_by_role("button", name="Submit").click()
    page.screenshot(path="screenshots/dark_add_tag_after.png", full_page=True)
    # delete tag
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("link", name="Terror").click()
    page.screenshot(path="screenshots/dark_delete_tag.png", full_page=True)
    # add description
    page.get_by_role("link", name="Add one?").click()
    page.get_by_label("Description").fill("Brian O'Conner, back working for the FBI in Los Angeles.")
    page.screenshot(path="screenshots/dark_add_description_before.png", full_page=True)
    page.get_by_role("button", name="Submit").click()
    page.screenshot(path="screenshots/dark_add_description_after.png", full_page=True)
