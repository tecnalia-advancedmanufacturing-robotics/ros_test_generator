#!/usr/bin/env python
"""
@package ros_test_generator
@file generate_xml.py
@author Anthony Remazeilles
@brief Generate xml file given a package model

Copyright (C) 2020 Tecnalia Research and Innovation
Distributed under the Apache 2.0 license.

"""

from ros_model_parser.rosmodel_parser import RosModelParser
from rospkg import RosPack
from jinja2 import Environment, FileSystemLoader, exceptions

import os


def main():
    print "Hello world"

    rp = RosPack()
    model_path = os.path.join(rp.get_path("ros_model_parser"),"resources/cob_light.ros")
    rossystem_parser = RosModelParser(model_path, isFile=True)

    static_model = rossystem_parser.parse()

    package_name = static_model.get("pkg_name")
    node_name = static_model.get("node_name")
    publishers = static_model.get("publishers")
    subscribers = static_model.get("subscribers")
    svr_servers = static_model.get("svr_servers")
    svr_clients = static_model.get("svr_clients")

    print "Package name: %s" % package_name
    print "Node name: %s" % node_name
    if publishers is not None:
        print "Publishers: "
        for pub in publishers:
            print"    Name: %s Type: %s" %(pub.get("name"), pub.get("type"))
    if subscribers is not None:
        print "Subscribers: "
        for sub in subscribers:
            print"    Name: %s Type: %s" %(sub.get("name"), sub.get("type"))
    if svr_servers is not None:
        print "Service Servers: "
        for svr in svr_servers:
            print"    Name: %s Type: %s" %(svr.get("name"), svr.get("type"))
    if svr_clients is not None:
        print "Service Clients: "
        for svr in svr_clients:
            print"    Name: %s Type: %s" %(svr.get("name"), svr.get("type"))

    # generating the dictionary as required.

    # for now we test all publishers
    cfg = {'author_name': 'Anthony Remazeilles',
        'author_email': 'Anthony.Remazeilles@tecnalia.com',
        'test_pkg_name': 'test_' + package_name[0] + '_' + node_name[0],
        'package_name': package_name[0],
        'node_name': node_name[0],
        'cyclic_publisher': list(),
        'publisher': list(),
        'dyn_param': list(),
        'filter': list(),
        'service': list()}

    for item in publishers:
        cfg['publisher'].append({'topic_name': item.get("name")[0]})
    for item in svr_servers:
        cfg['service'].append({'service_name': item.get("name")[0]})

    print "data for generation: %s" % cfg

    path_pattern = os.path.join(rp.get_path("ros_test_generator"), "pattern")

    template_environment = Environment(autoescape=False,
        loader=FileSystemLoader(path_pattern),
        trim_blocks=True)

    file_generated = template_environment.get_template("test.xml").render(cfg)

    print "generated file: \n %s" % file_generated
