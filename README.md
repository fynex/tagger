# tag.py
A basic file tagger

It is used to associate meta data to specific files, so that it is much easier to search for files. Furthermore, a fille can have multiple tags / classes, which is not that easy to create by using the directory structure. 

A config file will be safed in ```~/.tagger/default.json``` by default. 

The currently available usage looks like this (there are subparsers!):


```$ tag.py -h```
```
usage: tag.py [-h] [-w WORKSPACE] {add,search,remove,show,check,scan} ...

DESC

positional arguments:
  {add,search,remove,show,check,scan}
                        commands

optional arguments:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        A file name, which contains the tag data


```

```$ tag.py add -h```
```
python3 tag.py add -h
usage: tag.py add [-h] [-t TAG [TAG ...]] ADD

positional arguments:
  ADD                   The filename to add

optional arguments:
  -h, --help            show this help message and exit
  -t TAG [TAG ...], --tag TAG [TAG ...]
                        A tag name that associates a file

```
