from setuptools import setup, find_packages

setup(
    name='bitcoin_trading',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'websockets==12.0',
        'polars==1.2.1',
        'setuptools==71.1.0',
        'asyncio==3.4.3'
    ],
    entry_points={
        'console_scripts': [
            'bitcoin_trading=bitcoin_trading.main:main',
        ],
    },
    author='Arturo Gonzalez M.',
    author_email='arturo@arturosolutions.com.au',
    description='A project to process real-time cryptocurrency data from Binance using WebSocket API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/arturogonzalezm/bitcoin_trading',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.7',
)

