# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/20
@Software: PyCharm
@disc:
======================================="""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    packages=["django_celery_stack"],
    include_package_data=True,
    entry_points={
        'console_scripts': [

        ],
    },
)
