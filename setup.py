from setuptools import setup, find_packages

setup(name='beradio',
    version='0.5.0',
    description='BERadio',
    long_description='BERadio spec and reference implementation',
    classifiers=[
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: MQTT",
        "Topic :: Terminals :: Serial",
        "Programming Language :: Python",
    ],
    author='Hiveeyes Developers',
    author_email='he-devs@hiveeyes.org',
    url='',
    keywords='protocol rfm serial mqtt BERadio',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='beradio',
    install_requires=[
        'pyserial==2.7',
        'mosquitto==1.2.3',
        'bencode==1.0',
        'docopt==0.6.2',
        'appdirs==1.4.0',
        'json-store==2.1',
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
