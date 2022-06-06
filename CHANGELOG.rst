Changelog
=========


0.9.0 (2022-06-06)
------------------

* Fixed: upgrade urllib3
* Feature: support for application credentials
  
0.8.2 (2021-03-28)
------------------

* Fixed: upgrade dependencies (aiohttp)

0.8.1 (2019-04-03)
------------------

* Fixed: upgrade dependencies (urllib3: CVE-2018-20060)

0.8.0 (2018-08-19)
------------------

* Feature: another part of compute API - run an action on server
* Feature: CD configuration

0.7.0 (2018-06-15)
------------------

* Feature: Cinder implementation
* Bugfix: typo fixes

0.6.3 (2018-06-13)
------------------

* Feature: adjustable request timeout, default is 60s now


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

