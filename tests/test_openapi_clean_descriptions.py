from fastapi import FastAPI


def test_clean_multiline_openapi_descriptions():
    app_description = """
        Application description.

        ## Section

        - First item
            - Nested item
        """
    tag_description = """
        Tag description.

        ```python
        print("hello")
        ```
        """
    openapi_tags = [{"name": "items", "description": tag_description}]
    app = FastAPI(
        description=app_description,
        openapi_tags=openapi_tags,
    )

    schema = app.openapi()

    assert schema["info"]["description"] == (
        "Application description.\n"
        "\n"
        "## Section\n"
        "\n"
        "- First item\n"
        "    - Nested item"
    )
    assert schema["tags"][0]["description"] == (
        "Tag description.\n"
        "\n"
        "```python\n"
        'print("hello")\n'
        "```"
    )
    assert app.description == app_description
    assert app.openapi_tags == openapi_tags


def test_preserve_single_line_openapi_descriptions():
    app_description = "  Application description.  "
    tag_description = "  Tag description.  "
    openapi_tags = [{"name": "items", "description": tag_description}]
    app = FastAPI(
        description=app_description,
        openapi_tags=openapi_tags,
    )

    schema = app.openapi()

    assert schema["info"]["description"] == app_description
    assert schema["tags"][0]["description"] == tag_description
