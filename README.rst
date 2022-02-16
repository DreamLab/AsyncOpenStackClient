AsyncOpenStackClient
====================

|image0|_ |image1|_

.. |image0| image:: https://api.travis-ci.org/DreamLab/AsyncOpenStackClient.png?branch=master
.. _image0: https://travis-ci.org/DreamLab/AsyncOpenStackClient

.. |image1| image:: https://badge.fury.io/py/AsyncOpenStackClient.svg
.. _image1: https://badge.fury.io/py/AsyncOpenStackClient



Introduction
============

The `AsyncOpenStackClient` is a asynchronous rest wrapper for the OpenStack API. It provides a nice abstraction for authentication. For method specification, see the official OpenStack documentation: https://docs.openstack.org/queens/api/.


Installation
============

Use pip:

::

    pip install AsyncOpenStackClient


Usage
=====

.. code-block:: python

    from asyncopenstackclient import NovaClient, GlanceClient, CinderClient, AuthPassword

    # you can either pass credentials explicitly (as shown below)
    # or use environmental variables from OpenStack RC file
    # https://docs.openstack.org/mitaka/cli-reference/common/cli_set_environment_variables_using_openstack_rc.html
    auth = AuthPassword(
        auth_url='https://keystone:5999/v3'
        username='USER', password='PASS',
        project_name='my-project',
        user_domain_name='default',
        project_domain_name='foo.bar'
    )

    # alternatively you can also use application_credentials to authenticate with the OpenStack Keystone API
    # https://docs.openstack.org/keystone/queens/user/application_credentials.html
    alternative_auth = AuthPassword(
        auth_url='https://keystone:5999/v3'
        application_credential_id="ID",
        application_credential_secret="SECRET"
    )

    nova = NovaClient(session=auth)
    glance = GlanceClient(session=auth)
    cinder = CinderClient(session=auth)

    # api url for each service will be taken from catalog,
    # but you may pass `api_url` param to force custom url eg.
    # nova = NovaClient(session=auth, api_url='http://my-local-nova:9876/v2/')

    await nova.init_api()
    await glance.init_api()
    await cinder.init_api()


    servers = await nova.servers.list(name='testvm')
    vm = await nova.servers.get(server_id)

    action_spec = {'os-stop': None}
    await nova.servers.run_action(server_id, **action_spec)


    specs = {
        "name": 'some_name',
        "flavorRef": 'flavor_id',
        "imageRef": 'image_id',
        "security_groups": [{'name': 'group1'}, {'name': 'group2'}]
        "user_data": base64.b64encode(userdata).decode('utf-8')
    }
    response = await nova.servers.create(server=specs)
    print(response)

    volume = {"size": 200,
              "imageRef": "image_id",
              "name": "some_name"}

    response = await cinder.volumes.create(volume=volume)
    print(response)

Available functions
-------------------

- Nova (https://developer.openstack.org/api-ref/compute)

  - servers.list(optional=filter)  # params optional
  - servers.get(id)
  - servers.create(server=server_spec)
  - servers.force_delete(id)
  - servers.run_action(id, action=action_spec)
  - flavors.list()
  - metadata.get(server_id)
  - metadata.set(server_id, meta=meta_spec)
  - metadata.get_item(server_id, item_name)
  - metadata.set_item(server_id, item_name, meta=meta_spec)

- Glance (https://developer.openstack.org/api-ref/image/v2/index.html)

  - images.list()

- Cinder (https://developer.openstack.org/api-ref/block-storage/v3/index.html)

  - volumes.list(optional=filter)  # params optional
  - volumes.get(id)
  - volumes.create(volume=volume_spec)
  - volumes.force_delete(id)


License
=======

`Apache License 2.0 <LICENSE>`_
