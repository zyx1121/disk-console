from setuptools import setup, find_packages

setup(
    name='disk-monitor',
    version='0.1.1',
    author='Loki',
    author_email='yongxiang.zhan@outlook.com',
    description='A disk hex data monitor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zyx1121/disk-monitor',
    packages=find_packages(),
    install_requires=['rich'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'disk-monitor=disk_monitor.main:main',
        ],
    },
    zip_safe=False,
)