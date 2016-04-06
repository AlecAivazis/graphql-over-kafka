from invoke import run, task

def build_api_scripts():
    # the build targets
    script_src = 'nautilus/api/endpoints/static/src/scripts/graphiql.js'
    script_build = 'nautilus/api/endpoints/static/build/scripts/graphiql.js'
    # babel presents
    presets = ' '.join(['es2015', 'react', 'stage-0'])
    # the build command
    cmd = 'browserify %s -o %s -t [ babelify --presets [ %s ] ]' % (script_src, script_build, presets)
    # run the build command
    run(cmd)

def build_api_styles():
    # the build targets
    src_dir = 'nautilus/api/endpoints/static/src/styles'
    build_dir = 'nautilus/api/endpoints/static/build/styles'
    # the build command
    cmd = 'cp -r %s %s' % (src_dir, build_dir)
    # run the build command
    run(cmd)


@task
def build_static(docs=False):
    run('mkdir -p nautilus/api/endpoints/static/build/scripts/')
    build_api_scripts()
    build_api_styles()


@task
def build(docs=False):
    run('rm -rf dist')
    run('./setup.py sdist')
    run('./setup.py bdist_wheel')


@task
def deploy(docs=False):
    run('twine upload dist/*')
