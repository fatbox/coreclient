from distutils.core import setup

setup(
        name='coreclient',
        packages=['core'],
        version='0.2.2',
        license='BSD',
        description='Client libraries for accessing a CORE deployment',
        long_description=open('README').read(),
        author='Evan Borgstrom',
        author_email='evan@fatbox.ca',
        url='https://github.com/fatbox/coreclient',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            ],
        )
