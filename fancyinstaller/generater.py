import os
import zipfile, shlex, shutil
from kwargparse import ArgumentRequiredError
from .parser import kwargparser, get_python_origin
from .ifp_parser import write_ifp, CommandSlot


data_files_root = os.path.join(__file__, '../..', 'fancyinstaller-datafiles')
batch_start_template = '''@echo off
set PYTHON_ORIGIN=%s
set PACKAGES=%s'''

build_data_root = 'build/fancyinstaller-online'
contents_zip = os.path.join(build_data_root, 'contents.zip')
batch_script_name = os.path.join(build_data_root, 'online_install.cmd')
ifp_file = os.path.join(build_data_root, 'result.ifp')
output_file = os.path.join('dist', 'fancyinstaller-online-installer.ifp')


def generate_installer(**kwargs):
    kwargs = kwargparser.parse_kwargs(kwargs)
    if kwargs.modules is None:
        kwargs.modules = kwargs.packages
    if kwargs.version is None:
        try: kwargs.version = __import__(kwargs.modules[0]).__version__
        except (IndexError, AttributeError, ImportError):
            raise ArgumentRequiredError('argument %s required to be passed' % 'version') from None

    print('running generate_installer')
    if not os.path.exists(build_data_root):
        print('mkdir', build_data_root)
        os.makedirs(build_data_root)
    print('creating', contents_zip)
    zf = zipfile.ZipFile(contents_zip, 'w', zipfile.ZIP_DEFLATED)

    python_origin = get_python_origin(kwargs.python_version, kwargs.python_architecture, kwargs.python_origin)
    batch_script = batch_start_template % (python_origin, ' '.join(shlex.quote(package) for package in kwargs.packages))
    batch_script += '\n'
    with open(os.path.join(data_files_root, 'online_install.cmd')) as fp:
        batch_script += fp.read()
    print('writing', batch_script_name)
    with open(batch_script_name, 'w') as fp:
        fp.write(batch_script)
    print('copying', batch_script_name, '->', contents_zip)
    zf.write(batch_script_name, 'install.cmd')

    print('closing', contents_zip)
    zf.close()

    print('writing', ifp_file)
    with open(ifp_file, 'w') as fp:
        write_ifp(fp,
            name=kwargs.name,
            version=kwargs.version,
            zipfile=os.path.abspath(contents_zip),
            commands=[CommandSlot(command='<installpath>\\install.cmd', parameters='<installpath>', options='-wait')],
            program_relpath='python\\python.exe',
            program_arguments='-m ' + shlex.join(kwargs.modules[0]),
        )

    if not os.path.exists('dist'):
        print('mkdir', 'dist')
        os.mkdir('dist')
    print('copying', ifp_file, '->', output_file)
    shutil.copyfile(ifp_file, output_file)
    print('done')