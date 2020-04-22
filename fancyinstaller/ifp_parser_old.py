import configparser, tempfile

class IFP:
    def __init__(self):
        self._dict = configparser.ConfigParser()
        self.languages = []
        self.files_dirs = []
        self.license = b''
        self.registry = []
        self.variables = []
        self.shortcuts = []
        self.serials = []
        self.commands = []
    def parse(self, filename):
        # parse ini part
        temp_ifp = tempfile.TemporaryFile('w+')
        ifp = open(filename, 'r')
        for (ix, line) in enumerate(ifp):
            if ix >= 73: break
            temp_ifp.write(line)
        temp_ifp.seek(0)
        self._dict.read_file(temp_ifp)
        temp_ifp.close()
        del temp_ifp
        # parse languages
        for line in ifp:
            line = line.strip()
            if line == '[Files/Dirs]': break
            self.languages.append(int(line))
        # get license (not yet supported)
        ifp.readline()
        license_length = int(ifp.readline().strip())
        while line.strip() != '[Registry]':
            line = ifp.readline()
        del license_length
        # parse Registry
        current_registry = None
        for (ix, line) in enumerate(ifp):
            line = line.strip()
            if (ix % RegistrySlot.line_count) == 0:
                if current_registry is not None:
                    self.registry.append(RegistrySlot(*current_registry))
                current_registry = []
            if line == '[Variables]': break
            if ix % RegistrySlot.line_count == 4: line = bool(int(line))
            current_registry.append(line)
        del current_registry
        # parse Variables
        current_variables = None
        for (ix, line) in enumerate(ifp):
            line = line.strip()
            if (ix % RegistrySlot.line_count) == 0:
                if current_variables is not None:
                    self.variables.append(VariableSlot(*current_variables))
                current_variables = []
            if line == '[SCs]': break
            current_variables.append(line)
        del current_variables
        # parse SCs
        current_shortcuts = None
        for (ix, line) in enumerate(ifp):
            line = line.strip()
            if (ix % RegistrySlot.line_count) == 0:
                if current_shortcuts is not None:
                    self.variables.append(VariableSlot(*current_shortcuts))
                current_shortcuts = []
            if line == '[SCs]': break
            current_shortcuts.append(line)
        del current_shortcuts
    def generate(self, file):
        ifp = open(file, 'w')
        self._dict.write(ifp)
        ifp.write('[Languages]\n')
        ifp.write('\n'.join(str(x) for x in self.languages) + '\n')
        ifp.write('[License_Begin]\n')
        ifp.write(str(len(self.license)) + '\n')
        ifp.write(self.license.decode())
        ifp.write('[License_End]\n')
        ifp.write('[Registry]\n')
        ifp.write(''.join(x.as_string_block() for x in self.registry) + '\n')
        ifp.write('[Variables]\n')
        ifp.write(''.join(x.as_string_block() for x in self.variables) + '\n')
        ifp.write('[SCs]\n')
        ifp.write(''.join(x.as_string_block() for x in self.shortcuts) + '\n')
        ifp.write('[IFP_End]\n')
        ifp.write('[Serials]\n')
        ifp.write('\n'.join(str(x) for x in self.serials) + '\n')
        ifp.write('[Serials_End]\n')
        ifp.write('[Commands]\n')
        ifp.write(''.join(x.as_string_block() for x in self.commands) + '\n')
