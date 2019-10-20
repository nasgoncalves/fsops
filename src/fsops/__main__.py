#!/usr/bin/env python
from __future__ import (print_function)

import click

from atomicwrites import atomic_write
from path import Path

from fsops.fso import Object, Search


def render(fso, output_type):
    if output_type == 'json':
        return "{}\n".format(fso.to_json())

    elif output_type == 'parseble':
        return "{}\n".format(fso.to_parseble())

    raise Exception('not a valid output')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
@click.argument('db_path')
def diff(path, db_path):
    path = Path(path)
    db_path = Path(db_path)

    searched_objects = set(Search(path).walk())
    db_objects = {Object.from_json(o) for o in db_path.lines()}

    # diference between x to y
    new_objects = searched_objects - db_objects
    deleted_objects = db_objects - searched_objects

    # remove new files from searched
    for new_object in new_objects:
        searched_objects.remove(new_object)

    # files changed content
    changed_objects = set()

    for new_object in new_objects.copy():
        for db_object in db_objects:
            if (new_object.path == db_object.path
                    and new_object.hash != db_object.hash):
                new_objects.remove(new_object)
                changed_objects.add(new_object)

        for deleted_object in deleted_objects.copy():
            if deleted_object.path == new_object.path:
                deleted_objects.remove(deleted_object)

    # untouched files
    untouched_objects = set()
    for searched_object in searched_objects:
        untouched_objects.add(searched_object)

    for new_object in new_objects:
        print('new objects', new_object.path)

    for changed_object in changed_objects:
        print('changed objects', changed_object.path)

    for untouched_object in untouched_objects:
        print('untouched objects', untouched_object.path)

    for deleted_object in deleted_objects:
        print('delete objects', deleted_object.path)


@cli.command()
@click.argument('path')
@click.argument('save')
@click.option('--dbformat', default="json", help='Output type')
@click.option('--debug/--quiet', default=False)
def dump(path, save, dbformat, debug):
    path = Path(path)
    save = Path(save)

    click.echo('Path {}!'.format(path.abspath()))
    click.echo('Save Path {}'.format(save.abspath()))

    search = Search(path)

    with atomic_write(save, overwrite=True) as file_handler:
        try:
            for fso in search.walk():

                if debug:
                    print('\rprocessing {}\r'.format(fso.path))

                file_handler.write(render(fso, dbformat))
        except KeyboardInterrupt:
            file_handler.flush()
            click.echo('Closing database')


def main():
    cli()


if __name__ == '__main__':
    main()
