
from setuptools import setup

setup(
 name="beapicrawling",
 version="0.0.1",
 description="MICROSITE BE CRAWLING",
 author="beapicrawling",
 author_email="beapicrawling@multidayaintegra.com",
 license="GNU",
 url="https://github.com/multidayaintegra/beapicrawling",
 packages=["crawling/","crawling/crawling/","crawling/opensearch/","crawling/portalBerita",
 "crawling/portalBeritaV2/","crawling/portalTwitter/"],
 entry_points={
 "console_scripts": [
 "beapicrawling=beapicrawling:main",
 ]
 },
)