from setuptools import find_packages, setup

setup(
    name='BJUTLabServer',
    version='0.0.1',
    author="Woodykaixa",
    author_email="690750353@qq.com",
    description="Server-side application for BJUTLab Project, using Flask",
    packages=find_packages(),
    url='https://github.com/Woodykaixa/BJUTLabServer',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_cors'
    ],
    python_requires='>=3.6',
)
