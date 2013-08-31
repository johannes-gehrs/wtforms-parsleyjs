"""
This is a small library which you can hook into your WTForms form classes in order to
enable client side validation.

WTForms allows you to validate your forms on the server side. Ideally, we could reuse
these validators on the client side with JavaScript without writing any extra code. This
will allow for more direct user feedback in our forms.

This library uses ParsleyJS for this task. ParsleyJS is a popular client side
JavaScript validation library. It is configured using specific HTML markup in the forms.

This library will generate these attributes from your WTForms validators.

For more information consult the README.md in the Github repository at
https://github.com/johannes-gehrs/wtforms-parsleyjs

"""
from setuptools import setup

setup(
    name='WTForms-ParsleyJS',
    version='0.1.2',
    url='https://github.com/johannes-gehrs/wtforms-parsleyjs',
    license='MIT',
    author='Johannes Gehrs',
    author_email='jgehrs@gmail.com',
    description='Generate client side, parsley.js validation attributes automatically '
                'from WTForms server side validators.',
    long_description=__doc__,
    py_modules = ['run_sample'],
    packages=['wtformsparsleyjs', 'wtformsparsleyjs.sample'],
    platforms='any',
    install_requires=[
        'WTForms>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
