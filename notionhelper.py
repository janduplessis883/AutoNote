import autonote_config as ac
from notion_client import Client
import pprint


class NotionHelper:
    """
    Class NotionHelper
    ------------------
    A class to assist in interfacing with the Notion API.

    Methods:
    - __init__(self): Initializes an instance of the class and invokes the authenticate method.
    - authenticate(self): Sets the `notion_token` property equal to the `ac.notion_api_key` and creates a `Client` instance with the `notion_token` property to be used for queries.
    - notion_search_db(self, database_id='e18e2d110f9e401eb1adf3190e51a21b', query=''): Queries a Notion database and returns the page title and url of the result(s) page. If there are multiple results, pprint module is used to pretty print the results.
    - notion_get_page(self, page_id): Retrieves a Notion page and returns the heading and an array of blocks on that page.

    Usage:
    - Instantiate a `NotionHelper` object.
    - Call the `notion_search_db` method to search for pages in a Notion database.
    - Call the `notion_get_page` method to retrieve a page and its blocks.
    """

    def __init__(self):
        self.authenticate()

    def authenticate(self):
        # Authentication logic for Notion
        self.notion_token = ac.notion_api_key
        self.notion = Client(auth=self.notion_token)

    def notion_search_db(
        self, database_id="e18e2d110f9e401eb1adf3190e51a21b", query=""
    ):
        my_pages = self.notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "title",
                    "rich_text": {
                        "contains": query,
                    },
                },
            }
        )

        page_title = my_pages["results"][0]["properties"][
            "Code / Notebook Description"
        ]["title"][0]["plain_text"]
        page_url = my_pages["results"][0]["url"]

        page_list = my_pages["results"]
        count = 1
        for page in page_list:
            try:
                print(
                    count,
                    page["properties"]["Code / Notebook Description"]["title"][0][
                        "plain_text"
                    ],
                )
            except IndexError:
                print("No results found.")

            print(page["url"])
            print()
            count = count + 1

        # pprint.pprint(page)

    def notion_get_page(self, page_id):
        """Returns the heading and an array of blocks on a Notion page given its page_id."""

        page = self.notion.pages.retrieve(page_id)
        blocks = self.notion.blocks.children.list(page_id)
        heading = page["properties"]["Subject"]["title"][0]["text"]["content"]
        content = [block for block in blocks["results"]]

        print(heading)
        pprint.pprint(content)
