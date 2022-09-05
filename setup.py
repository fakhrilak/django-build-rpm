
from setuptools import setup

setup(
 name="beapicrawling",
 version="0.0.1",
 description="CRAWLING ENGINE RPM VERTION",
 author="beapicrawling",
 author_email="beapicrawling@zilog.online.com",
 license="GNU",
 url="https://github.com/multidayaintegra/beapicrawling",
 packages=["beapicrawling/","beapicrawling/crawling/","beapicrawling/opensearch/","beapicrawling/portalBerita",
 "beapicrawling/portalBeritaV2/","beapicrawling/portalTwitter/"],
 entry_points={
 "console_scripts": [
 "beapicrawling=beapicrawling:main",
 ]
 },
)