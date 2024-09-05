Version 0.9.0
-------------
* Use uv for packaging and building
* Drop Python 3.8
* Remove CursesMenu.append_item

Version 0.8.3
-------------
* Minor fixes

Version 0.8.2
-------------
* Minor fixes
* Dependency updates

Version 0.8.1
-------------
* Fixed dependencies on Windows

Version 0.8.0
-------------
*Changed parameter name in itemGroup
*Dev dependencies updated

Version 0.7.0
-------------
* Drop Python 3.7

Version 0.6.14
-------------
* Updating deployment workflow
* Various dependency and testing updates

Version 0.6.11
-------------
* Fix issue with calling stty
* Various dependency and testing updates

Version 0.6.10
-------------
* Testing automatic deployment

Version 0.6.9
-------------
* Update dev dependencies
* Fix dependabot complaint in test/doc dependency

Version 0.6.8
-------------
* Added some more pre-commit checks
* Update dependencies for security fix in documentation build

Version 0.6.7
-------------
* Test on release python 3.11
* Fix readme

Version 0.6.5
-------------
* Fix bug caused by not having Deprecated as install dependency.

Version 0.6.5
-------------

* Use Poetry, some github actions changes. Not pushing this one to pypi.

Version 0.6.4
-------------

* Workaround vscode/windows-curses issue

Version 0.6.3
-------------

* Actually fixed bug that breaks doc build

Version 0.6.2
-------------

* Fixed bug that breaks doc build

Version 0.6.1
-------------

* Mostly just fixed bugs in tests
* Improved cross-platform functionality of CommandItem

Version 0.6.0
-------------

* Large rewrite and refactor of pretty much everything
* 100% test coverage
* Started using pre-commit for style
* Migrated from Travis to Github actions
* Type checking with mypy
* Better handling of exit item via item groups
* Some ability to test/debug the actual graphical output
* Fixed bugs
