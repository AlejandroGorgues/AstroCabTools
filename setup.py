from setuptools import setup, find_packages
from os import path

absPath = path.abspath(path.dirname(__file__))

with open(path.join(absPath, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='astroTools',
	version='1.0.0',
	author='Alejandro',
	author_email='email',
	url='url',
	description='description',
	packages=['all_tools/src',
		'mrs_chan/src',
		'mrs_spec_chan/src',
		'mrs_det_plot/src',
		'fit_line'],
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
		'PyPubSub>=4.0.3'
	],
	entry_points={
		'gui_scripts':[
			'allTools = all_tools.src.all_tools:main',
			'fitLine = fit_line.src.main:main',
			'detPlot = mrs_det_plot.src.main:main',
			'specChan = mrs_spec_chan.src.main:main',
			'bandChan = mrs_chan.src.main:main'
		],
	}
)
