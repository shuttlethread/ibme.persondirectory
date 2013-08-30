from setuptools import setup, find_packages


version = '1.1'


setup(
    name='ibme.persondirectory',
    version=version,
    description='Directory of people',
    long_description=open("README.rst").read() + "\n" +
                     open("docs/HISTORY.txt").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python"],
    keywords='plone person directory',
    author='Jamie Lentin',
    author_email='jamie.lentin@shuttlethread.com',
    url='http://shuttlethread.com',
    license='',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ibme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.contentlisting',
        'plone.app.dexterity',
        'plone.indexer',
        ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
    )
