from setuptools import setup, find_packages

setup(
    name="omero-vitessce",
    version="1.2.2",
    description="OMERO Vitessce multimodal data viewer plugin for OMERO.web",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Michele Bortolomeazzi',
    author_email='michele.bortolomeazzi@dfkf.de',
    license='AGPLv3',
    url="https://github.com/MicheleBortol/omero-vitessce",
    python_requires='>=3.9',
    packages=find_packages(),
    install_requires=["vitessce==3.3.0", "shapely==2.0.6"],
    keywords=["OMERO.web", "OMERO", "Vitessce", "viewer"],
    include_package_data=True,
)
