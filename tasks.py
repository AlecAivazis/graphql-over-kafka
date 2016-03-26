from invoke import run, task



@task
def build(docs=False):
    run('rm -rf dist')
    run('./setup.py sdist')
    run('./setup.py bdist_wheel')


@task
def deploy(docs=False):
    run('twine upload dist/*')
