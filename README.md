# capstone
### Objective
* Harvest application to scrape web pages for information and download files
     * The application saves website information into a database and stores the downloaded files to disk
* Create a REST API which accepts file submissions.
     * The application extracts metadata from file uploads and allows users to read the metadata, update/correct the metadata and delete submissions.

### Functional Requirements

#### Harvest Application
 
* The application crawls the webpage (http://3.228.218.197/). The application should save all the links on the index page and be able to determine when new links are added if the website is updated.
* The application should also download the programs linked in the download page.
* The application should also save certain information on the current download page. If there's a change on the information, the application should download the program again.
* The information that can change are the following:
  * program name
  * program version
* The application should then submit the downloaded file to the REST API and record the response in the DB.
 
#### REST API
 
* The application extracts metadata from a file submission and stores the data in a PostgreSQL database.
* The files are stored in a directory in the hosting machine. The application should reject duplicate file submissions.
* The following attributes are extracted from files:
  - size, filename, sha1, md5, filetype (note that submissions may not include filenames
* The application should allow clients to retrieve the metadata via SHA-1 or MD5.
* It should also allow clients to update the metadata for a specific file.
* The application should allow clients to delete an entry which also deletes the actual file stored in the machine.

### Nonfunctional Requirements
* Docker must be installed on a CentOS 7 VM installed from scratch and configured properly so that the application/REST API can be accessed by the host machine.

* The applications should be running in a docker container so that deployment and dependencies are easily managed. The REST API also use WSGI server to handle HTTP connections.

* Unit tests should have at least 80% coverage.

* The final code should be committed in a GitHub repository named "capstone"
