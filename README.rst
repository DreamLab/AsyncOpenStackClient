AsyncOpenstakClient
===================

|image0|_

.. |image0| image:: https://api.travis-ci.org/DreamLab/AsyncOpenStackClient.png?branch=master
.. _image0: https://travis-ci.org/DreamLab/AsyncOpenStackClient


Introduction
============

The `AsyncOpenStakClient` is rest wrapper to OpenStack API. It provides very raw functionality however, it has a nice abstraction for authetication. For method specification go to official OpenStack reference https://docs.openstack.org/queens/api/.


Installation
============

Use pip:

::

    pip install AsyncOpenStackClient


Usage
=====

As mentioned above this is "raw" library, so you must handle `params` and/or `body` and the `response`.


.. code-block:: python

    from asyncopenstackclient import NovaClient, GlanceClient, AuthPassword

    auth = AuthPassword(
        auth_url='https://keystone:5999/v3'
        username='USER', password='PASS',
        project_name='my-project',
        user_domain_name='default',
        project_domain_name='foo.bar'
    )
    nova = NovaClient(session=auth)
    glance = GlanceClient(session=auth)

    # api url for each service will be taken from catalog,
    # but you may pass `api_url` param to force custom url eg.
    # nova = NovaClient(session=auth, api_url='http://my-local-nova:9876/v2/')

    await nova.init_api()
    await glance.init_api()


    servers = await nova.api.servers.list(params={'name': 'testvm'})
    vm = await nova.api.servers.get(id)


    body = {
        "server": {
            "name": 'some_name',
            "flavorRef": 'flavor_id',
            "imageRef": 'image_id',
            "security_groups": [{'name': 'group1'}, {'name': 'group2'}]
            "user_data": base64.b64encode(userdata).decode('utf-8')
        }
    }
    response = await nova.api.servers.create(body=body)
    print(response.body)


Available functions
-------------------

- Nova (https://developer.openstack.org/api-ref/compute)

  - servers.list(params)  # params optional
  - servers.get(id)
  - servers.create(body)
  - servers.force_delete(id)
  - flavors.list()

- Glance (https://developer.openstack.org/api-ref/image/v2/index.html)

  - images.list()


License
=======

`Apache License 2.0 <LICENSE>`_
