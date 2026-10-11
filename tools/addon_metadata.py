"""Format the game's addon-list metadata from the publication configuration."""


def addon_description(publication, character):
    descriptions = publication["editions"][character]["addon_description"]
    parts = [descriptions[language].strip() for language in ("en", "zh-CN")]
    if any(not part or '"' in part or "\0" in part for part in parts):
        raise ValueError("Addon descriptions must be nonempty text without quotes or NULs")
    # An actual newline is valid inside a quoted KeyValues string. Do not emit
    # a literal backslash-n, which some addon-info readers display as text.
    return "\n".join(parts)


def addoninfo_text(publication, character, version):
    title = publication["editions"][character]["title"]
    author = publication["maintainer"]
    for value in (title, author, version):
        if not value or any(token in value for token in ('"', "\0", "\n", "\r")):
            raise ValueError("Invalid single-line addon metadata")
    description = addon_description(publication, character)
    return f'''"AddonInfo"
{{
    "addonSteamAppID" "550"
    "addonTitle" "{title}"
    "addonVersion" "{version}"
    "addonAuthor" "{author}"
    "addonDescription" "{description}"
}}
'''
