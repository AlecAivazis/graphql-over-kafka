# external imports
import os
import errno
from jinja2 import Template

def render_template(template, out_dir='.', context=None):
    '''
        This function renders the template desginated by the argument to the
        designated directory using the given context.

        Args:
            template (string) : the source template to use (relative to ./templates)
            out_dir (string) : the name of the output directory
            context (dict) : the template rendering context
    '''
    # the directory containing templates
    template_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      '..',
                                      'templates',
                                      template
                                     )

    # the files and empty directories to copy
    files = []
    empty_dirs = []

    for (dirpath, _, filenames) in os.walk(template_directory):
        # if there are no files in the directory
        if len(filenames) == 0:
            # add the directory to the list
            empty_dirs.append(os.path.relpath(dirpath, template_directory))
        # otherwise there are files in this directory
        else:
            # add the files to the list
            files.extend([os.path.join(dirpath, filepath) for filepath in filenames])

    # for each template file
    for source_file in files:
        # open a new file that we are going to write to
        with open(source_file, 'r') as file:
            # create a template out of the source file contents
            template = Template(file.read())
            # render the template with the given contents
            template_rendered = template.render(**(context or {}))

            # the location of the source relative to the template directory
            source_relpath = os.path.relpath(source_file, template_directory)

            # the target filename
            filename = os.path.join(out_dir, source_relpath)
            # create a jinja template out of the file path
            filename_rendered = Template(filename).render(**context)

            # the directory of the target file
            source_dir = os.path.dirname(filename_rendered)
            # if the directory doesn't exist
            if not os.path.exists(source_dir):
                # create the directories
                os.makedirs(source_dir)

            # create the target file
            with open(filename_rendered, 'w') as target_file:
                # write the rendered template to the target file
                target_file.write(template_rendered)

    # for each empty directory
    for dirpath in empty_dirs:
        try:
            # dirname
            dirname = os.path.join(out_dir, dirpath)
            # treat the dirname as a jinja template
            dirname_rendered = Template(dirname).render(**context)

            # if the directory doesn't exist
            if not os.path.exists(dirname_rendered):
                # create the directory in the target, replacing the name
                os.makedirs(dirname_rendered)
        except OSError as exc:
            # if the directory already exists
            if exc.errno == errno.EEXIST and os.path.isdir(dirpath):
                # keep going (noop)
                pass
            # otherwise its an error we don't handle
            else:
                # pass it along
                raise
