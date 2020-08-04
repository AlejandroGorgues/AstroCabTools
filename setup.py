from setuptools import setup, find_packages
from os import path
from io import open

absPath = path.abspath(path.dirname(__file__))

with open(path.join(absPath, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='AstroCabTools',
	version='0.9.6',
	author='Alejandro Gorgues',
	description='Set of analysis tools of MRS data',
        long_description=long_description,
        long_description_content_type='text/markdown',
	package_dir={'src':'mrs_chan',
		'src':'mrs_spec_chan',
		'src':'mrs_det_plot',
		'src':'fit_line',
                'src':'all_tools'},
	packages=['astrocabtools/mrs_chan/src',
		'astrocabtools/mrs_spec_chan/src',
		'astrocabtools/mrs_det_plot/src',
		'astrocabtools/fit_line/src',
                'astrocabtools/all_tools/src'],
	include_package_data=True,
	classifiers=[
		'Programming Language :: Python :: 3.7',
	],
	python_requires='>=3.7',
	install_requires=[
		'matplotlib>=3.1.3',
		'astropy>=4.0',
		'PyQt5>=5.14',
		'numpy>=1.18.1',
		'seaborn>=0.9.0',
		'lmfit>=1.0.0',
                'PyPubSub>=4.0.3',
	],
	entry_points={
		'gui_scripts':[
			'fitLine = astrocabtools.fit_line.src.main:main',
			'detPlot = astrocabtools.mrs_det_plot.src.main:main',
			'specChan = astrocabtools.mrs_spec_chan.src.main:main',
			'bandChan = astrocabtools.mrs_chan.src.main:main',
                        'allTools = astrocabtools.all_tools.src.all_tools:main',
		],
	}
)
