#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse


class Tagger:

    def __init__(self, data_path):
        self.data_path = data_path
        self.data      = {}


    def read_data(self):
        if os.path.isfile(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        else:
            with open(self.data_path, "w") as f:
                f.write("{}")


    def write_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)


    def add_file(self, tag, filepath):
        absolute_path = os.path.abspath(filepath)

        if not tag in self.search_tag(tag).values():
            #self.data[tag] = self.search_tag(tag) + [absolute_path]
            self.data[absolute_path] = sorted(set(self.search_path(absolute_path) + [tag]))
        else:
            #self.data[tag] = [absolute_path]
            self.data[absolute_path] = [tag]


    def search_path(self, path):
        try:
            return self.data[path]
        except KeyError:
            return []


    def search_tag(self, tag):
        paths_with_tag = {}

        for path,tags in self.data.items():
            if tag in tags:
                paths_with_tag[path] = tags

        return paths_with_tag


    def search_multi_tag(self, tag_list):
        sub_dict = {}

        for path,tags in self.data.items():
            for other_tag in tag_list:
                if othertag in tags:
                    sub_dict[path] = tags

        return sub_dict


    def search_tag_substr(self, tag, substr):
        found_paths = {}

        for path,tags in self.data.items():
            if substr in path:
                if tag in tags:
                    found_paths[path] = tags

        return found_paths


    def search_multi_tag_substr(self, tag_list, substr):
        found_paths = {}

        for tag in tag_list:
            found_paths.update( self.search_tag_substr(tag, substr) )

        return found_paths


    def remove_tag_substr(self, tag, substr):
        files = self.search_tag(tag)

        for filepath in files:
            if substr in filepath:
                index = files.index(filepath)
                del files[index]


    def remove_path(self, substr_path):
        for path in self.data.keys():
            if substr_path in path:
                del self.data[path]
                break


    def check_files(self):
        for filepath in self.data.keys():
            if not os.path.isfile(filepath):
                index = files.index(filepath)
                del files[index]


    def __str__(self):
        string = ""

        for filepath,tags in self.data.items():
            string += "{}\t{}\t{}\n".format(tags, os.path.basename(filepath), filepath)
        #string = str(self.data)

        return string



## Main ##
parser     = argparse.ArgumentParser(description="DESC")
subparsers = parser.add_subparsers(help='commands', dest='command')
add        = subparsers.add_parser('add')
search     = subparsers.add_parser('search')
remove     = subparsers.add_parser('remove')
show       = subparsers.add_parser('show')
check      = subparsers.add_parser('check')
scan       = subparsers.add_parser('scan') #TODO scan all subdirs in the current dir an search for data specified in a config file: *.nmap => scan, file type pdf => info

remove.add_argument("remove", metavar='REMOVE', help="The filename to add")
remove.add_argument("-t", "--tag", help="A tag name that associates a file")

add.add_argument("add", metavar='ADD', help="The filename to add")
add.add_argument("-t", "--tag", nargs="+", help="A tag name that associates a file")

search.add_argument("search", metavar='SEARCH', help="The tag names to search for")
search.add_argument("-s", "--substring", help="Searches for a substring the tagged data")

parser.add_argument("-w", "--workspace", help="A file name, which contains the tag data")

show.add_argument("show", metavar='SHOW', default="", nargs='?', help="The filename to add")

args = parser.parse_args()

workspace = args.workspace

if not args.workspace:
    path = "{}/.tagger/".format(os.path.expanduser("~"))

    if not os.path.exists(path):
        os.makedirs(path)

    workspace = "{}default.json".format(path)


tagger = Tagger(workspace)
tagger.read_data()


if args.command == "add":
    tags     = args.tag
    filepath = args.add

    for tag in tags:
        tagger.add_file(tag, filepath)

elif args.command == "search":
    tag_list = args.search
    substr   = args.substring

    found_values = tagger.search_multi_tag(tag_list)
    print(found_values)

elif args.command == "remove":
    tag    = args.tag
    substr = args.remove

    if not tag:
        #sys.exit("[!] You must provide a substring")
        tagger.remove_path(substr)
    else:
        tagger.remove_tag_substr(tag, substr)

elif args.command == "show":
    filterword = args.show

    if filterword == "tags":
        for t in tagger.data.keys():
            print(t)
    else:
        print(tagger)

elif args.commmand == "check":
    tagger.check_files()

tagger.write_data()

