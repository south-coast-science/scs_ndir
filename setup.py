from setuptools import setup, find_packages


with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]

setup(
    name='scs_ndir',
    version='0.1.0',
    description='Environmental sampling abstractions for the South Coast Science NDIR SPI board.',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs_ndir',
    package_dir={'':'src'},
    packages=find_packages('src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3",
)