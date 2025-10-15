from setuptools import setup

setup(
    name='CLAUDIO',
    version='v2.0.0',
    packages=['claudio', 'claudio.utils', 'claudio.data', 'claudio.module01', 'claudio.module01.src',
              'claudio.module01.src.io', 'claudio.module01.src.algorithm', 'claudio.module02',
              'claudio.module02.src_structure_search', 'claudio.module02.src_structure_search.io',
              'claudio.module02.src_structure_search.algorithm', 'claudio.module02.src_distance_reevaluation',
              'claudio.module02.src_distance_reevaluation.io', 'claudio.module02.src_distance_reevaluation.algorithm',
              'claudio.module03', 'claudio.module03.src', 'claudio.module03.src.io', 'claudio.module03.src.algorithm',
              'claudio.module04', 'claudio.module04.src', 'claudio.module04.src.io', 'claudio.module04.src.algorithm'],
    url='https://github.com/ElhabashyLab/CLAUDIO-2.0',
    license='MIT',
    platforms='Windows/Linux/Mac',
    author='Alexander Röhl, Tobias Löser',
    author_email='alexander.roehl@uni-tuebingen.de, tobias.loeser@student.uni-tuebingen.de',
    description='Structural analysis, mapping, validation, visualization, and modeling of protein cross-links on '
                'protein and protein-protein interaction.',
    install_requires=['biopython==1.79', 'click==8.1.3', 'matplotlib==3.6.3', 'pandas==1.5.3', 'requests==2.28.2','numpy==2.0.0'],
    include_package_data=True,
    package_data={'': ['data/*']},
    entry_points={
        'console_scripts': [
            'claudio=claudio.claudio:main',
            'claudio_lists=claudio.module01.src.main:main',
            'claudio_structdi=claudio.module02.run_module02_intra:main',
            'claudio_ops=claudio.module03.src.main:main',
            'claudio_xl=claudio.module04.src.main:main'
        ]
    }
)
