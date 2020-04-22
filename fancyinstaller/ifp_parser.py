ifp_template = '''[Header]
ProjectFileVersion = "1.1"
[General]
Program name = %(name)s
Program version = %(version)s
Windows 2000 = 1
Windows XP = 1
Windows Server 2003 = 1
Windows Vista = 1
Windows Server 2008 = 1
Windows 7 = 1
Windows 8 = 1
Windows 10 = 1
Windows Server 2016 = 1
DoNotCheckOS = 1
Company name = %(company_name)s
Website = %(website)s
SFA = 0
DFA = 0
Comp = 1
[Graphics]
Wizard image = <main>
Header image = <main>
Install-icon image = <main>
Show Label = 1
Windows style = 1
XpStyle = 1
[Files]
Include Zipfile = %(include_zipfile)i
Zipfile = %(zipfile)s
Installation path = <programfiles>\\<company>\\<appname>\\
Autcip = 1
[Uninstall]
Vwau = 0
Website = 
Include uninstaller = %(include_uninstaller)i
Uninstaller filename = Uninstall
[Licence]
Licence dialog = 0
[Finish]
Sart program = 0
Reboot computer = 0
Execute DLL: = 0
Program = <installpath>\\%(program_relpath)s
ProgramArguments = %(program_arguments)s
Dll = 
[Shortcuts]
Allowtc = 1
Shortcut path = <company>\\<appname>\\
[Serialoptions]
Allows = 0
Number = 20
[SplashScreen]
Image = 
Sound = 
Time = 2
PlaySound = 0
Allow = 0
[Build]
File = 
[Updater]
Allow = 0
1 = <appname>
2 = <appversion>
3 = http://
4 = http://
5 = http://
6 = Update
Language = 0
RunProg = 
RunProgs = 0
Execdlls = 0
[Languages]
%(languages)s[Files/Dirs]
[Licence_Begin]
1
\0[Licence_End]
[Registry]
%(registry)s[Variables]
%(variables)s[SCs]
%(shortcuts)s[IFP_End]
[Serials]
[Serials_End]
[Commands]
%(commands)s'''


def write_ifp(fp, name='', version='', company_name='', website='http://', include_zipfile=True,
              zipfile='', include_uninstaller=False, program_relpath='', program_arguments='',
              languages=[], registry=[], variables=[], shortcuts=[], commands=[]):
    data = ifp_template % dict(
        name = name,
        version = version,
        company_name = company_name,
        website = website,
        include_zipfile = include_zipfile,
        zipfile = zipfile,
        include_uninstaller = include_uninstaller,
        program_relpath = program_relpath,
        program_arguments = program_arguments,
        languages = '\n'.join(str(x) for x in languages),
        registry = '\n'.join(x.as_string_block() for x in registry),
        variables = '\n'.join(x.as_string_block() for x in variables),
        shortcuts = '\n'.join(x.as_string_block() for x in shortcuts),
        commands = '\n'.join(x.as_string_block() for x in commands),
    )
    fp.write(data)
    return data
    


class RegistrySlot:
    line_count = 5
    def __init__(self, root_key='HKET_CLASSES_ROOT', sub_key='', value_name='', value_data='', remove_when_uninstalling=False):
        self.root_key = root_key
        self.sub_key = sub_key
        self.value_name = value_name
        self.value_data = value_data
        self.remove_when_uninstalling = remove_when_uninstalling
    def as_string_block(self):
        return '\n'.join(
            self.root_key,
            self.sub_key,
            self.value_name,
            self.value_data,
            int(self.remove_when_uninstalling),
        )

class VariableSlot:
    line_count = 5
    def __init__(self, variable_name='', root_key='HKEY_CLASSES_ROOT', sub_key='', value_name='', default_value=''):
        self.variable_name = variable_name
        self.root_key = root_key
        self.sub_key = sub_key
        self.value_name = value_name
        self.default_value = default_value
    def as_string_block(self):
        return '\n'.join(
            self.variable_name,
            self.root_key,
            self.sub_key,
            self.value_name,
            self.default_value,
        )

class ShortcutSlot:
    line_count = 6
    def __init__(self, destination='Desktop', shortcut_name='', target_file='<installpath>\\', command_line_arguments='', icon_file='', icon_index=0):
        self.destination = destination
        self.shortcut_name = shortcut_name
        self.target_file = target_file
        self.command_line_arguments = command_line_arguments
        self.icon_file = icon_file
        self.icon_index = icon_index
    def as_string_block(self):
        return '\n'.join(
            self.destination,
            self.shortcut_name,
            self.target_file,
            self.command_line_arguments,
            self.icon_file,
            self.icon_index,
        )

class CommandSlot:
    line_count = 4
    def __init__(self, type='Execute application', command='<installpath>\\', parameters='', options=None):
        if options is None:
            if type == 'Execute application':
                options = '-wait -hide'
            else: options = ''
        self.type = type
        self.command = command
        self.parameters = parameters
        self.options = options
    def as_string_block(self):
        return '\n'.join(
            self.type,
            self.command,
            self.parameters,
            self.options,
        )

if __name__ == '__main__':
    # print(ifp.registry)
    # print('\n'.join(x.as_string_block() for x in ifp.variables))
    write_ifp(open('out.ifp', 'w'))