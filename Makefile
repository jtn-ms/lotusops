
# ~/.pypirc
# [distutils]
# index-servers =
#     pypi
#     testpypi
# [testpypi]
# repository = https://test.pypi.org/legacy/
# username = testpypi.username
# password = testpypi.password

# [pypi]
# repository = https://upload.pypi.org/legacy/
# username = pypi.username
# password = pypi.password

pypi.register:
	@python3 setup.py register

pypi.upload:
	@python3 setup.py sdist upload

# [version.control]
# lotusops/__init.py:__version__=<new_version>
# git tag <new_version>
# git push origin --tags
# git tag -d <tagname>
# git push --delete origin <tagname>