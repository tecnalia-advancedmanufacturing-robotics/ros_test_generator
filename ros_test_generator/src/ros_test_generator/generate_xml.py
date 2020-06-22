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

import argparse
import os
import sys
import copy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", '-m', required=True, type= str, help='node model')
    parser.add_argument("--out", '-o', required=True, type= str,  help='generated test spec')

    args = parser.parse_args()

    generate_xml(args.model, args.out)


def ask_for_cyclic_pub(pubs):

    cyclic_pubs = list()
    if not pubs:
        return cyclic_pubs

    # not for python 2.7...
    #l_pubs = pubs.copy()
    l_pubs = copy.deepcopy(pubs)

    print "Identified %d publishers" % len(l_pubs)

    for id, item in enumerate(l_pubs):
        print "[{}] name: {}".format(id, item['topic_name'])

    is_cyclic = raw_input("Is there some cyclic publisher [y/n]")

    is_cyclic = is_cyclic.lower()
    yes = {'y', 'yes'}

    while is_cyclic in yes:
        print "cyclic defined"
        for id, item in enumerate(l_pubs):
            print "[{}] name: {}".format(id, item['topic_name'])

        id_pub, freq = raw_input("Provide publisher id, and desired frecuency. -1 to end: ").split()

        id_pub = int(id_pub)
        if id_pub >= len(l_pubs):
            print "id_pub should be integer in [0, %d]" % (len(l_pubs) - 1)
            continue

        if id_pub < 0:
            break

        item = {'topic_name': l_pubs[id_pub]['topic_name'],
                'frequency': freq}
        # print "Adding: {}".format(item)
        cyclic_pubs.append(item)
        del l_pubs[id_pub]

        is_cyclic = raw_input("Other cyclic publisher [y/n]")
        is_cyclic = is_cyclic.lower()

    return cyclic_pubs


def ask_for_filter_mode(pubs, subs):

    filter_pubs = list()
    if not pubs or not subs:
        return filter_pubs

    # not for python 2.7...
    # l_pubs = pubs.copy()
    l_pubs = copy.deepcopy(pubs)
    l_subs = copy.deepcopy(subs)

    print "Identified %d publishers, and %d subscribers" % (len(l_pubs), len(l_subs))

    for id, item in enumerate(l_subs):
        print "sub [{}] name: {}".format(id, item['topic_name'])

    for id, item in enumerate(l_pubs):
        print "pub [{}] name: {}".format(id, item['topic_name'])
    is_filter = raw_input("Is there some filter like sub pub relation? [y/n]: ")

    is_filter = is_filter.lower()
    yes = {'y', 'yes'}

    while is_filter in yes:
        print "filter defined"

        for id, item in enumerate(l_subs):
            print "sub [{}] name: {}".format(id, item['topic_name'])

        for id, item in enumerate(l_pubs):
            print "pub [{}] name: {}".format(id, item['topic_name'])

        id_sub, id_pub = raw_input("Provide subscriber_id, publisher id, -1 to end: ").split()

        id_pub = int(id_pub)
        id_sub = int(id_sub)

        if id_pub < 0 or id_sub < 0:
            break

        if id_pub >= len(l_pubs):
            print "id_pub should be integer in [0, %d]" % (len(l_pubs) - 1)
            continue
        if id_sub >= len(l_subs):
            print "id_pub should be integer in [0, %d]" % (len(l_subs) - 1)
            continue

        item = {'topic_in': l_subs[id_sub]['topic_name'],
                'topic_out': l_pubs[id_pub]['topic_name']}
        # print "Adding: {}".format(item)
        filter_pubs.append(item)

        is_filter = raw_input("Other filter like sub-pub connexion [y/n]")
        is_filter = is_filter.lower()

    return filter_pubs


def generate_xml(model_file, output_file):

    # rp = RosPack()
    # model_path = os.path.join(rp.get_path("ros_model_parser"),"resources/cob_light.ros")
    rossystem_parser = RosModelParser(model_file, isFile=True)

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
        'subscriber': list(),
        'dyn_param': list(),
        'filter': list(),
        'service': list()}

    for item in publishers:
        cfg['publisher'].append({'topic_name': item.get("name")[0]})
    for item in subscribers:
        cfg['subscriber'].append({'topic_name': item.get("name")[0]})
    for item in svr_servers:
        cfg['service'].append({'service_name': item.get("name")[0]})

    print "data for generation: %s" % cfg

    cfg['cyclic_publisher'] = ask_for_cyclic_pub(cfg['publisher'])
    cfg['filter'] = ask_for_filter_mode(cfg['publisher'], cfg['subscriber'])

    rp = RosPack()
    path_pattern = os.path.join(rp.get_path("ros_test_generator"), "pattern")

    template_environment = Environment(autoescape=False,
        loader=FileSystemLoader(path_pattern),
        trim_blocks=True)

    file_generated = template_environment.get_template("test.xml").render(cfg)

    print "generated file: \n %s" % file_generated
    with open(output_file, 'w') as out_file:
            out_file.write(file_generated)

    print "You can now generate the test package:"
    print "rosrun package_generator generate_package {}".format(output_file)
