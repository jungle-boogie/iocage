"""Common methods we reuse."""


def sort_tag(tag):
    """Sort the list by tag."""
    list_length = len(tag)

    # Length 8 is list -l, 7 is df, 5 is list
    if list_length == 8:
        _tag = tag[4]
    elif list_length == 7:
        _tag = tag[6]
    elif list_length == 5:
        _tag = tag[3]
    else:
        _tag = tag[1]

    _sort = _tag.rsplit('_', 1)

    # We want to sort tags that have been created with count > 1. But not
    # foo_bar
    if len(_sort) > 1 and _sort[1].isdigit():
        return _sort[0], int(_sort[1])
    else:
        return _tag, 0


def sort_release(releases, split=False):
    """
    Sort the list by RELEASE, if split is true it's expecting full
    datasets.
    """
    release_list = []

    if split:
        for rel in releases:
            rel = float(rel.split("/")[3].split()[0].split("-")[0])
            release_list.append(rel)
    else:
        for release in releases:
            if "-RELEASE" in release:
                release = float(release.split("-")[0])
                release_list.append(release)

    release_list.sort()

    for r in release_list:
        index = release_list.index(r)
        release_list.remove(r)

        if split:
            # We want these sorted, so we cheat a bit.
            release_list.insert(index, ["{}-RELEASE".format(r)])
        else:
            # We want these sorted, so we cheat a bit.
            release_list.insert(index, "{}-RELEASE".format(r))

    return release_list
