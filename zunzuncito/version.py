"""Version

major.minor.commits
"""
version_commits = 6.648

VERSION_TUPLE = (0, 1, int(version_commits))

__version__ = '.'.join(map(str, VERSION_TUPLE))
