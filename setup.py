import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyserial==2.7',
    'paho-mqtt==1.3.1',
    'bencode==1.0',
    'docopt==0.6.2',
    'appdirs>=1.4.0',
    'json-store==2.1',
    # 'terkin==0.0.1',
]

test_requires = [
    'nose==1.3.7',
    'coverage==4.0.1',
]

setup(name='beradio',
    version='0.12.0',
    description='BERadio',
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Terminals :: Serial",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    author='The Hiveeyes Developers',
    author_email='hello@hiveeyes.org',
    url='https://hiveeyes.org/docs/beradio/',
    keywords='protocol rfm serial mqtt Bencode BERadio',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='beradio',
    install_requires=requires,
    tests_require=test_requires,
    extras_require={
        'test': test_requires,
    },
    entry_points={
        'console_scripts': [
            'beradio            = beradio.commands:beradio_cmd',
            'bdecode            = beradio.commands:bdecode_cmd',
            'bencode            = beradio.commands:bencode_cmd',
            'bemqtt             = beradio.commands:bemqtt_cmd',
        ],
    },
)
