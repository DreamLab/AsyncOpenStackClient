Changelog
=========

0.6.2 (2018-05-18)
------------------

* Bugfix: initialize property (api) in Client to get some meaningful error instead of "recursion limit reached".


0.6.0 (2018-05-12)
------------------

* Feature: wrap requests with Resource/Method proxy


0.5.2 (2018-05-10)
------------------

* Bugfix: adding slash at the end of api_root_url


0.5.1 (2018-04-29)
------------------

* Bugfix: update README with metadata entry and envs notice


0.5.0 (2018-04-25)
------------------

* Feature: partial support for server metadata usage


0.4.1 (2018-04-25)
------------------

* Bugifx: invalid concat auth_url with urljoin


0.4.0 (2018-04-16)
------------------

* Feature: use `OS_` variables if present


0.3.0 (2018-04-13)
------------------

* Feature: accept to pass api_url
* Feature: determine api url if catalog provide incomplete one (eg. without version)


0.2.3 (2018-04-05)
------------------

* Bugfix: do_not_await_sync_method


0.2.2 (2018-04-02)
------------------

* Update simple-rest-client (fixed logging)


0.2.1 (2018-03-28)
------------------

* fix tests, cov report,  MANIFEST.in


0.1.1 (2018-03-02)
------------------

* Update MANIFEST.in

0.1.0 (2018-02-15)
------------------

* First approach to build async openstack client library for Python3

