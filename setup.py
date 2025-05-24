from setuptools import setup, find_packages

setup(
    name="recruitment-screener",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "streamlit>=1.31.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
)