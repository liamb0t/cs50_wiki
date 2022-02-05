import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_edit(absolute_path):
    """
    Gets relative path from absolute path from previous page URL. 
    Workaround until I figure out why hidden form in displayEntry.html 
    is not working.
    """
    abs_path = str(absolute_path)
    rel_path = ''
    i = 1
    while abs_path[-i] != '/':
        rel_path += abs_path[-i]
        i += 1
    rel_path = rel_path[::-1].replace('%20', ' ')
    return rel_path
