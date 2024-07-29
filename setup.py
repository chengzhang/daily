"""
sgame_nlp_data 安装脚本

Author: donyzhang
Date: 2024-07-10
Update: 2024-07-10
"""

# coding = utf8

import os

from setuptools import find_packages, setup

current_dir = os.path.dirname(os.path.realpath(__file__))


def requirements():
    packages = []
    with open(os.path.join(current_dir, 'requirements.txt')) as ins:
        for line in ins:
            line = line.strip()
            if line and not line.startswith('#'):
                packages.append(line)
    return packages


def readme():
    with open(os.path.join(current_dir, 'README.md')) as ins:
        description = ins.read()
        return description


setup(
    name='sgame_nlp_data',
    version='0.0.1',
    description='王者 nlp 数据工程',
    long_description=readme(),
    keywords='nlp, data',
    project_urls={
        'Documentation': 'https://git.woa.com/sgame_nlp/sgame_nlp_data/README.md',
        'Source': 'https://git.woa.com/sgame_nlp/sgame_nlp_data',
        'Tracker': 'https://git.woa.com/sgame_nlp/sgame_nlp_data/issues',
    },
    entry_points={
        'console_scripts': [
            'sgame_nlp_data_cmd = sgame_nlp_data.bin.command:cli'
        ]
    },
    packages=find_packages(),
    package_data={'sgame_nlp_data': ['config/settings.json']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Natural Language :: Chinese',
    ],
    url='https://git.woa.com//nlptools',
    author='donyzhang',
    author_email='https://git.woa.com/sgame_nlp/sgame_nlp_data',
    tests_require=['pytest'],
    install_requires=requirements(),
    python_requires='>=3.8, <4',
    zip_safe=False
)
