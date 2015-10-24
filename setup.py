from setuptools import setup, find_packages

setup(name='beradio',
    version='0.0.3',
    description='BERadio',
    long_description='BERadio spec and reference implementation',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: MQTT",
        "Topic :: Terminals :: Serial",
    ],
    author='',
    author_email='',
    url='',
    keywords='protocol rfm serial mqtt BERadio',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='beradio',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'beradio            = beradio.commands:beradio_cmd',
            'bdecode            = beradio.commands:bdecode_cmd',
            'bencode            = beradio.commands:bencode_cmd',
        ],
    },
)
