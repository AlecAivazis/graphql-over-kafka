#! /usr/bin/env python3

# external imports
from os import system as run
import click

# the group of commands
@click.group()
def command_group(): pass


@command_group.command()
def build_api_scripts():
    run('mkdir -p nautilus/api/endpoints/static/build/scripts/')
    # the build targets
    script_src = 'nautilus/api/endpoints/static/src/scripts/graphiql.js'
    script_build = 'nautilus/api/endpoints/static/build/scripts/graphiql.js'
    # babel presents
    presets = ' '.join(['es2015', 'react', 'stage-0'])
    # the build command
    build_cmd = 'browserify %s -t [ babelify --presets [ %s ] ]' % (script_src, presets)
    # the command to minify the code
    minify_cmd = 'uglifyjs'
    # minify the build and put the result in the right place
    run('%s | %s > %s' % (build_cmd, minify_cmd, script_build))
    # let the user know we're finished
    print("Successfully built api script files.")


@command_group.command()
@click.pass_context
def build_static(context):
    # call the underlying functions
    context.forward(build_api_scripts)


@command_group.command()
def build(docs=False):
    run('rm -rf dist')
    run('./setup.py sdist')
    run('./setup.py bdist_wheel')


@command_group.command()
def deploy(docs=False):
    run('twine upload dist/*')


# if executing this file from the command lien
if __name__ == '__main__':
    # start the command group
    command_group()
