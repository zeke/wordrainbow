Setup
-----

The static portion of the site is built with ruby's staticmatic.
Staticmatic doesn't let you configure the output directory, so we're using 
a rake task to copy static files from /staticmatic/site to /web_py/

	./staticmatic/rake build

Bugs
----

* MIME type headers; see http://cl.ly/5Vdy
* static assets not always loading correctly
* show well-known color names first

Wishlist
--------

* Design the "Identify" section
* Design the "Visualize" section
* Don't allow saving unless color has been changed
* Remove sensitive stuff from the app so it can be open-sourced

Discoveries
-----------

* API users can't read other users' lists. They should be able to.
* Public users don't have access to tagging of any kind
* WordLists cannot be sorted
* WordList items cannot contain metadata
* The documentation for word.{format}/{word}/tag is lacking
* can't tag a word more than once with the same tag (?)
* can't get tags for a word
* Robin's API needs to support PUT, POST, DELETE, etc.

Credentials
-----------

repo: https://github.com/zeke/wordrainbow
username: wordrainbow
passowrd: g....
api_key: 1d3ba...
