from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='postgrey',
    version='0.0.1',
    description='🐘 Simple, Fast, Async & ORM PostgreSQL database client based on Asyncpg for Python.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/5elenay/postgrey/',
    author='5elenay',
    author_email='',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/5elenay/postgrey/issues",
    },
    classifiers=classifiers,
    keywords=["postgres", "postgresql", "orm", "database", "client", "fast", "asyncio"],
    packages=find_packages(),
    python_requires='>=3.6.0',
    install_requires=["asyncpg"]
)