
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

pypi.upload: uninstall
	@python3 setup.py sdist
	@read -p "type username(pypi.org):" username;\
	 read -p "type password(pypi.org): " password;\
	 python3 -m twine upload -u$$username -p$$password --repository pypi dist/*

# python3 setup.py install
install:
	@python3 setup.py build
	@pip install ./

clean:
	@rm -rf __pycache__ dist lotusops.egg-info build *.pyc

uninstall: clean
	@rm -rf /usr/local/lib/python3.6/dist-packages/lotusops*
	@python3 -m pip uninstall lotusops

# [version.control]
# lotusops/__init.py:__version__=<new_version>
# git tag <new_version>
# git push origin --tags
# git tag -d <tagname>
# git push --delete origin <tagname>

# wrong meta type totally broke twine
# it returns with TypeError: expected string or bytes-like object for any call for twine
# >>> import importlib_metadata as md
# >>> dists = md.distributions()
# >>> broken = [dist for dist in dists if dist.name is None]
# >>> for dist in broken:
# ...     print(dist._path)
# ...     print('metadata length', len(dist.metadata()))
# solution:
# rm -rf /usr/local/lib/python3.6/dist-packages/lotusops* 
