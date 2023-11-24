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

def search(entry_lsts, page_to_be_found):
    result = [False, []]
    print(entry_lsts)
    potential_lst = list(filter(lambda v: re.match(f'.*{page_to_be_found}.*', v.lower()), entry_lsts))
    correct_lst = list(filter(lambda v: re.match(f'{page_to_be_found}', v.lower()), entry_lsts))

    # correct_lst = list(filter(lambda v: v == page_to_be_found), potential_lst)
    if len(correct_lst) == 1:
        result[0] = True
        result[1] = correct_lst
    else:
        result[1] = potential_lst
    return result
