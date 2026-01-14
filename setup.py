from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="tej",
    version="1.0.0",
    description="ERPNext app for Tunisian Fiscal Declarations (Tej - RS & CbC)",
    author="Mehdi Khechine",
    author_email="mehdi@erpbox.online",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
