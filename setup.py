from setuptools import setup

setup(
    name="manga scrap",
    version="0.0.1",
    author="Italo Maia",
    author_email="italo.maia@gmail.com",
    description="API for dealing with web comic sites",
    license="MIT",
    keywords="comics manga webtoon",
    packages=["manga_scrap"],
    install_requires=[
        "gevent",
        "parsel",
    ],
    test_requires=[
        'pytest',
        'pytest-pythonpath',
    ]
)
