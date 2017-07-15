from setuptools import setup, find_packages

setup(name='beradio',
    version='0.11.0',
    description='BERadio',
    long_description='BERadio spec and reference implementation',
    license="GPL 3",
    classifiers=[
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: MQTT",
        "Topic :: Terminals :: Serial",
        "Programming Language :: Python",
    ],
    author='Hiveeyes Developers',
    url='https://hiveeyes.org/docs/beradio/',
    keywords='protocol rfm serial mqtt Bencode BERadio',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='beradio',
    install_requires=[
        'pyserial==2.7',
        'paho-mqtt==1.2',
        'bencode==1.0',
        'docopt==0.6.2',
        'appdirs>=1.4.0',
        'json-store==2.1',
        #'terkin==0.0.1',
    ],
    entry_points={
        'console_scripts': [
            'beradio            = beradio.commands:beradio_cmd',
            'bdecode            = beradio.commands:bdecode_cmd',
            'bencode            = beradio.commands:bencode_cmd',
            'bemqtt             = beradio.commands:bemqtt_cmd',
        ],
    },
)
