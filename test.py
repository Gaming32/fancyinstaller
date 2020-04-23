from fancyinstaller import generate_installer

generate_installer(
    name = 'Uno',
    packages = [
        'Uno-Game',
    ],
    modules = [
        'uno',
    ],
)