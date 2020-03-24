import sys
import kwargparse, semantic_version

def VersionType(obj):
    if isinstance(obj, semantic_version.Version):
        return obj
    else: return semantic_version.Version.coerce(obj)
def IterableType(obj):
    for _ in obj: return obj
def ArchitectureType(obj):
    if obj in ('x86', '32', 32):
        return 32
    elif obj in ('x86_64', 'x64', '64', 64):
        return 64
    else: raise ValueError('invalid architecture %r' % obj)

def get_python_origin(version, architecture, origin):
    if origin is not None:
        return origin
    if version is None:
        version = '.'.join(str(p) for p in sys.version_info[:3])
    if architecture == 64:
        architecture = 'amd64'
    else: architecture = None
    return 'https://www.python.org/ftp/python/%s/python-%s%s.exe' % (
        version, version, ('-' + str(architecture) if architecture else ''))

kwargparser = kwargparse.KeywordArgumentParser()
kwargparser.add_argument('name', type=str)
kwargparser.add_argument('version', default=semantic_version.Version('1.0.0'), type=VersionType)
kwargparser.add_argument('packages', type=IterableType, default=[])
kwargparser.add_argument('modules', type=IterableType, required=False)
kwargparser.add_argument('include_updater', 'include-updater', type=bool, default=True)
kwargparser.add_argument('update_dependencies', 'update-dependencies', type=IterableType, default=[])
kwargparser.add_argument('python_version', 'python-version', required=False)
kwargparser.add_argument('python_architecture', 'python-architecture', default='x86', type=ArchitectureType)
kwargparser.add_argument('python_origin', 'python-origin', required=False)