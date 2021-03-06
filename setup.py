import os
import re
from glob import glob
import shutil
from setuptools import setup, find_packages, Extension
from setuptools import Distribution, Command
from setuptools.command.install import install



#TODO: fill in these
__pkg_name__ = 'medaka'
__author__ = 'syoung'
__description__ = 'Neural network sequence error correction.'

__path__ = os.path.dirname(__file__)
__pkg_path__ = os.path.join(os.path.join(__path__, __pkg_name__))

verstrline = open(os.path.join(__pkg_name__, '__init__.py'), 'r').read()
vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(vsre, verstrline, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in "{}/__init__.py".'.format(__pkg_name__))


dir_path = os.path.dirname(__file__)
install_requires = []
with open(os.path.join(dir_path, 'requirements.txt')) as fh:
    reqs = (
        r.split('#')[0].strip()
        for r in fh.read().splitlines() if not r.strip().startswith('#')
    )
    for req in reqs:
        if req.startswith('git+https'):
            req.split('/')[-1].split('@')[0]
    install_requires.append(req)

exes = ['samtools', 'minimap2', 'mini_align']

setup(
    name='medaka',
    version=__version__,
    url='https://github.com/nanoporetech/{}'.format(__pkg_name__),
    author=__author__,
    author_email='{}@nanoporetech.com'.format(__author__),
    description=__description__,
    packages=find_packages(),
    package_data={
        __pkg_name__:[os.path.join('data','*.hdf5')],
    },
    install_requires=install_requires,
    #place binaries as package data, below we'll copy them to standard path in dist
    data_files=[
        ('exes', [
            'bincache/{}'.format(x, x) for x in exes
        ])
    ],
    entry_points = {
        'console_scripts': [
            '{0} = {0}.{0}:main'.format(__pkg_name__),
            'hp_compress = {0}.{1}:main'.format(__pkg_name__, 'compress'),
            'medaka_data_path = {0}.{1}:{2}'.format(__pkg_name__, 'common', 'print_data_path'),
        ]
    },
    scripts=['scripts/medaka_consensus'],
    zip_safe=False,
)


# Nasty hack to get binaries into bin path
print("\nCopying utility binaries to your path.")
class GetPaths(install):
    def run(self):
        self.distribution.install_scripts = self.install_scripts
        self.distribution.install_libbase = self.install_libbase

def get_setuptools_script_dir():
    # Run the above class just to get paths
    dist = Distribution({'cmdclass': {'install': GetPaths}})
    dist.dry_run = True
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()

    print(dist.install_libbase)
    src_dir = glob(os.path.join(dist.install_libbase, 'medaka-*', 'exes'))[0]
    for exe in (os.path.join(src_dir, x) for x in os.listdir(src_dir)):
        print("Copying", os.path.basename(exe), '->', dist.install_scripts)
        shutil.copy(exe, dist.install_scripts)
    return dist.install_libbase, dist.install_scripts

get_setuptools_script_dir()

