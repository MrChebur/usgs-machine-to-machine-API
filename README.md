![Image](https://repository-images.githubusercontent.com/283676892/ae1b6b80-0d41-11eb-9098-3ebca41f480b)
Simple Python wrapper of the USGS/EROS Inventory Service Machine-to-Machine API as described in the [documents](https://m2m.cr.usgs.gov/api/docs/json/).

----------------------------------------
**UPDATE 2024.12.06**
* All USGS methods, data types and errors are now consistent with the USGS API.
* All USGS data types are now classes. Use `.dict` to convert them to a dictionary.
* Type hits added to USGS methods and data types.
* The old USGS `login` method will be deprecated in February 2025 (a warning has been added).
----------------------------------------
> [!IMPORTANT]
> 
> You must have machine-to-machine access to execute queries.
> You can order access [here](https://ers.cr.usgs.gov/profile/access). 
----------------------------------------
**INSTALLATION**
```
pip install https://github.com/MrChebur/usgs-machine-to-machine-API/archive/master.zip
```
----------------------------------------
**CODE EXAMPLES**

See another code example [here](https://github.com/MrChebur/usgs-machine-to-machine-API/blob/master/examples/UsageExample.py). 
```python
from usgs_m2m.usgsMethods import API as M2M

api = M2M()
api.loginToken('usgs_username', 'usgs_token')
permissions = api.permissions()
print(permissions)
# {
#     'requestId': '00000000', 
#     'version': 'stable', 
#     'sessionId': '00000000', 
#     'data': ['user', 'download', 'order'],
#     'errorCode': None, 
#     'errorMessage': None
# }
```
----------------------------------------