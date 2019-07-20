
# Introduction
The goal of this project is to provide a easy way to run selenium
tests just with some webpage and JSON knowledge

# What does it do ?
using a simple json configuration file you can run tests for your webpage.
<br>Some features you could use:
 - taking screenshot during the testing
 - developer console check for error codes (ideal for api communication)
 - logging the whole process
 - multiple ways to select an element
 - background processing of the test (no need of GUI or supervisor during the process)

# But can it run Mozilla ?
At this moment the only browser core is Chrome. For future, my goal
is to add support for more browser cores.
<br>?? It is possible adding support manually, just edit /lib/tester.py ;) ??

 # Requirements
- Python3
- pip3
- Chrome web browser
- valid configuration file

# Instalation
- this installation expects, that you meet all the requirements
1) clone this repository (or pull if you already have)
2) `pip3 install -r requirements.txt` if its necessary run as `sudo`
3) copy `chromedriver` to `/usr/local/bin` - `sudo cp chromedriver /usr/local/bin/chromedriver`
4) ` sudo chmod 0777 /usr/local/bin/chromedriver`
5) create `tests` folder
6) edit path and config name in `main.py`
- Ready to GO !!

# Configuration
 - All the configuration of the run is either in your configuration json file (more further) or in the `main.py` file
 - configuration file contains all the steps and paths for the test and `main.py` contains the path to the configuration file and location of the script


# Running a test
- For this task you will need to create a configuration file describing
all the steps and attributes of your test
- after creating a valid configuration file you run `sudo python3 main.py`

# Creating configuration
- configuration file consists of three main parts:
<br> 1) Whole test attributes (folder paths, url, name)
<br> 2) Test which will run during this main process. One test can contain multiple runs with different paths ;)
<br> 3) List of steps contained in the above mentioned run
- an example of the configuration file is provided in this repository `config_example.json`

## Test attributes
```json
{
  "name":"String // Name of test - just for organizing ('Some test')",
  "url":"String // The URL we will be testing",
  "paths":{
    "test":"String // Folder for test results and files",
    "screens":"String // Folder for screen storing",
    "logs":"String // Folder for logs output"
  },
  "tests":["Array of objects // Array containing runs - more in next example"]
}
```
## Run atrributes

```json
{
  "name":"String // name of the run",
  "folder":"String // name of folder for storing run data",
  "screenshot":"Boolean // take screenshot in every step of run",
  "initial_errors":"Array of string // if present, will test for errors in console - example: ['500', '403']",
  "stages":["Array of objects // list of steps in run - more in next example"]
}
```
## Run steps
- run can contain a check for console errors with simple attribute  `error_control`
- `error_control` will be an array of codes which should be checked for after end of the step

```json
{
  "error_control":["500","404","300"]
}
```

- whole example of `error_control` usage

```json
{
  "type":"path",
  "selector":"//*[@id=\"login-form\"]/div/form/button",
  "action":"click",
  "continue_on":{
    "element":"#loader"
  },
  "error_control":["500","404","300"]
}
```
### Run can contain multiple type of interaction

### wait
  - is used for longer waiting times or just to stop the process of testing for a while
  - wait can be set to multiple conditions which need to be fulfilled to continue

    #### 'element'
    - in this case the run will continue after the element is visible on page

    ```json
    {
      "type":"wait",
      "continue_on":{
        "element":".someelement"
      }
    },
    ```
    #### 'not_element'
    - in this case the run will continue after the element is not visible anymore

    ```json
    {
      "type":"wait",
      "continue_on":{
        "not_element":".someelement"
      }
    },
    ```

    #### 'clickable'
    - in this case the run will continue after the element is clickable (not overlapped)

    ```json
    {
      "type":"wait",
      "continue_on":{
        "clickable":".someelement"
      }
    },
    ```

    #### 'time'
    - in this case the run will continue after elapsed time in seconds

    ```json
    {
      "type":"wait",
      "continue_on":{
        "time":"20"
      }
    },
    ```

### path
- use `path` when you need a more complicated XPath selector for item selection
- after `path` you specify `action` attribute (click or input) and if you choose `input` you need to specify `value` attribute too
- this type is recommended for situations where you can not provide a simple class or id selector, in this situations use only path
     #### input
     ```json
     {
       "type":"path",
       "value":"some random value",
       "selector":"//*[@id=\"hp-app\"]/div/div[1]/div[2]/div/label/input",
       "action":"input",
       "continue_on":{
         "time":5
       }
     }
     ```
     #### click
     ```json
     {
       "type":"path",
       "action":"click",
       "selector":"//*[@id=\"hp-app\"]/div/div[1]/div/div/button/span[1]",
       "continue_on":{
         "time":20
       }
     }
     ```

### button
- buttons only use is to make click action on provided selector.
- selector must be `.class` or `#id`
```json
{
  "type":"button",
  "selector":"#login",
  "continue_on":{
    "element":"#login-form"
  }
},
```

### input
- inputs is only use is to insert value in to an input field
- selector must be `.class` or `#id`
```json
{
  "type":"input",
  "value":"someRandomValue",
  "selector":"#loginFormUsername",
  "continue_on":{
    "time":5
  }
}
```


# Next steps
- run in Docker 
- resolution for test enviroment 
- random Agents
- Tor support

### Used stuff
  https://chromedriver.storage.googleapis.com/index.html?path=2.44/
  https://sites.google.com/a/chromium.org/chromedriver/getting-started
