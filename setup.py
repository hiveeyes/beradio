import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()
# CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    "pyserial<4",
    "paho-mqtt<2",
    "bencode.py<5",
    "docopt<1",
    "appdirs<2",
    "json-store<4",
    # 'terkin==0.0.1',
]

test_requires = [
    "nose2<1",
    "nose2-cov==1.0a4",
    "jsonpointer<3",
    "PyYAML<7",
    "u-msgpack-python<3",
]

setup(
    name="beradio",
    version="0.13.0",
    description="BERadio is an encoding specification and implementation for efficient "
    "communication in constrained radio link environments. It is conceived "
    "and used for over-the-air communication within the Hiveeyes project.",
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Terminals :: Serial",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    author="The Hiveeyes Developers",
    author_email="hello@hiveeyes.org",
    url="https://hiveeyes.org/docs/beradio/",
    keywords="protocol rfm serial mqtt Bencode BERadio",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="beradio",
    install_requires=requires,
    tests_require=test_requires,
    extras_require={
        "test": test_requires,
    },
    entry_points={
        "console_scripts": [
            "beradio            = beradio.commands:beradio_cmd",
            "bdecode            = beradio.commands:bdecode_cmd",
            "bencode            = beradio.commands:bencode_cmd",
            "bemqtt             = beradio.commands:bemqtt_cmd",
        ],
    },
)
