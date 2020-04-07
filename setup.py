from setuptools import setup

setup(name='aws_utils',
      version='0.0.1',
      description='Wrapper to interact with AWS through Boto3',
      url='https://github.com/matbloch/aws_utils',
      author='Matt',
      author_email='matthias@github.com',
      license='MIT',
      packages=['aws_utils'],
      install_requires=[
          'boto3',
      ],
      zip_safe=False)