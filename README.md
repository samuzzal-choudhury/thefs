# THEFS
_A file store application_

## Introduction
THEFS (short for `The File Store`) is a simple text file store service that supports the following operations:

* Add new files
* Update an existing file
* List all files present in the store
* Remove an existing file from the store
* Generate the cumulative word count of the entire file store.
* Generate 'n' most or least frequently occuring words in the file store.

This repo come with a command line 'store' (located in the `cmd` directory) to perform the above operations by communicating with the API service.

The Following are the usage info of the command line tool

```
$ store -h
usage: store [-h] {add,update,ls,wc,remove,freq-words} ...

Command line tool for API operations

positional arguments:
  {add,update,ls,wc,remove,freq-words}
    add                 Upload files
    update              Update a single file
    ls                  List files on the server
    wc                  Generate the total word count of all files
    remove              Delete a file
    freq-words          Generate the "n" most or least frequently occuring words in the file store

options:
  -h, --help            show this help message and exit 
```

There are a few optional arguments for the `freq-words` command. 

```
$ store freq-words -h
usage: store freq-words [-h] [-n LIMIT] [-o {asc,dsc}]

options:
  -h, --help            show this help message and exit
  -n LIMIT, --limit LIMIT
                        Limit of frequent words
  -o {asc,dsc}, --order {asc,dsc}
                        Order of the frequent words
```

## Deploying the API service

### Using docker-compose

From the project root after cloning this repo:

```
$ docker-compose build

$ docker images
REPOSITORY            TAG       IMAGE ID       CREATED          SIZE
thefs_thefs           latest    74bf95640f4f   34 seconds ago   206MB

$ docker-compose up -d
Creating network "thefs_default" with the default driver
Creating thefs_thefs_1 ... done

$ docker-compose ps
    Name                Command            State                    Ports                  
-------------------------------------------------------------------------------------------
thefs_thefs_1   flask run --host=0.0.0.0   Up      0.0.0.0:5000->5000/tcp,:::5000->5000/tcp

$ docker-compose logs
Attaching to thefs_thefs_1
thefs_1  |  * Serving Flask app 'main.py'
thefs_1  |  * Debug mode: off
thefs_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
thefs_1  |  * Running on all addresses (0.0.0.0)
thefs_1  |  * Running on http://127.0.0.1:5000
thefs_1  |  * Running on http://172.20.0.2:5000
thefs_1  | Press CTRL+C to quit

$ cd cmd
$ export PATH:$PATH:.
```

### Using local kind cluster

From the project root after cloning the project

```
$ cd k8s
$ kubectl apply -f deployment-api.yaml
$ kubectl apply -f service-api.yaml
$ kubectl get po

$ kubectl get po
NAME                               READY   STATUS    RESTARTS   AGE
thefs-deployment-5ff8879c8-qf6mg   1/1     Running   0          25m

$ kubectl get service

$ kubectl get service
NAME            TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
thefs-service   LoadBalancer   10.96.32.69   <pending>     5000:30491/TCP   19m

$ kubectl get no -o yaml
…
  status:
    addresses:
    - address: 172.18.0.3
      type: InternalIP
…
```

Set the API_URL_BASE based on the node IP

```
$ cd ../cmd
$ export PATH:$PATH:.
$ export API_BASE_URL=http://172.18.0.3:30491/api/v1
```

## Example run

```
$ cat test_store_cli 
store ls
store add ../sample_files/file1.txt
store add ../sample_files/file2.txt
store add ../sample_files/file2.txt
store update ../sample_files/file2.txt
store update ../sample_files/file3.txt
store ls
store wc
store freq-words -n 5 -o dsc
store freq-words -n 5 -o asc
store remove file1.txt
store remove file2.txt
store remove file3.txt
store ls
```

Example result:

```
No files
Response Status Code: 200
Response Body:
{'message': 'success'}
Response Status Code: 200
Response Body:
{'message': 'success'}
Response Status Code: 400
Error: {"error":"Received an existing file file2.txt"}

Response Status Code: 200
Response Body:
{'message': 'success'}
Response Status Code: 200
Response Body:
{'message': 'success'}
file3.txt
file2.txt
file1.txt
486
['TXT', 'and', 'a', 'files', 'or']
["you're", 'looking', 'testing', 'there', 'many']
Response Status Code: 200
Response Body:
{'status': 'successfully deleted file1.txt'}
Response Status Code: 200
Response Body:
{'status': 'successfully deleted file2.txt'}
Response Status Code: 200
Response Body:
{'status': 'successfully deleted file3.txt'}
No files

```

## Run Unit Tests

From the project root after cloning the repo

```
$ docker build -t thefs-test:latest -f Dockerfile.test .

$ docker run thefs-test
============================= test session starts ==============================
platform linux -- Python 3.12.4, pytest-8.2.2, pluggy-1.5.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /app
plugins: mock-3.14.0
collecting ... collected 6 items

tests/test_utils/test_files.py::test_store_file_success PASSED           [ 16%]
tests/test_utils/test_files.py::test_list_files PASSED                   [ 33%]
tests/test_utils/test_files.py::test_list_files_empty PASSED             [ 50%]
tests/test_utils/test_files.py::test_remove_file_success PASSED          [ 66%]
tests/test_utils/test_files.py::test_generate_words_frequency PASSED     [ 83%]
tests/test_utils/test_files.py::test_count_total_words PASSED            [100%]

============================== 6 passed in 0.15s ===============================

```

## Run linter and docstyle (Optionally)

From the project root after cloning the repo -

```
$ docker build -t thefs_lint_docstyle:latest -f Dockerfile.linter_docstyle .

$ docker run thefs_lint_docstyle
<no output in case of a successful run>
```

To see linter error(s), change the a line length of the files.py to more than 79

```
$ docker build -t thefs_lint_docstyle:latest -f Dockerfile.linter_docstyle .

$ docker run thefs_lint_docstyle
thefs/utils/files.py:49:80: E501 line too long (80 > 79 characters)
```
