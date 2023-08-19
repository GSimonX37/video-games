# Site parser backloggd.com
This program is designed to receive data by extracting it from the pages of the <a href=https://www.backloggd.com>backloggd.com</a> web resource.

## Program description
The parser is written using the aiohttp HTTP client library, which makes it possible to collect data asynchronously.

The parser itself consists of 5 managers, each of which performs its own tasks:
<ol>
    <li>Progress manager.
        <ul>
            <li>progress update;</li>
            <li>calculation of the current data processing speed;</li>
            <li>calculation of the remaining time, taking into account the current data processing speed.</li>
        </ul>
    </li>
    <li>File manager.
        <ul>
            <li>reading and writing data to a file;</li>
            <li>reading and writing a file with a checkpoint;</li>
            <li>calculate current file size;</li>
            <li>counting the number of records in a file.</li>
        </ul>
    </li>
    <li>Network manager.
        <ul>
            <li>sending requests to the server and receiving responses from it;</li>
            <li>counting the number and types of response statuses received from the server;</li>
            <li>calculate the volume of incoming traffic.</li>
        </ul>
    </li>
    <li>Delay manager.
        <ul>
            <li>control the delay before sending a request to the server.</li>
            <li>creating a more complex delay generation algorithm.</li>
        </ul>
    </li>
    <li>Proxy manager.
        <ul>
            <li>Proxy rotation (not implemented at this stage).</li>
        </ul>
    </li>
</ol> 

## Setting up and running the program

An example code that will allow you to extract data from a site looks like this:
``` python
import asyncio
import os
from parser import Parser


async def main():
    parser = Parser()

    if await parser.connect() == 200:
        if os.path.exists('checkpoint.json') and input('Load checkpoint (y/n): ') == 'y':
            await parser.load_checkpoint('checkpoint.json')
        else:
            await parser.file_manager_setting('output.csv', 'w')
            await parser.progress_manager_setting('main', [1, 4])
            await parser.network_manager_setting((5, 10))

        await parser.print_status()
        if not input('Press enter to start...'):
            await parser.run()

    await parser.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
```

The next line is needed to create a session object, with the help of which requests will be sent to the server in the future, and also to make sure that the server is available at the given moment.
``` python
if await parser.connect() == 200
```  
Also, after receiving all the data, it is necessary to close the session connection:
``` python
await parser.close_connection()
```  
Before you start collecting data, you should check the checkpoint file. This is necessary if the previous data collection was interrupted before it was completed and you want to continue from the last page.
``` python
if os.path.exists('checkpoint.json') and input('Load checkpoint (y/n): ') == 'y':
    await parser.load_checkpoint('checkpoint.json')
```
Before starting the scraping process, it is necessary to configure the parser managers by calling the following functions:
``` python
await parser.file_manager_setting('output.csv', 'w')
await parser.progress_manager_setting('main', [1, 4])
await parser.network_manager_setting((5, 10))
```  
## Setting up parser managers
### File manager
To configure the file manager, you need to call the configure_file_manager() method of the Parser class and pass two arguments to it: the complete file name and the mode of working with the file. For example:
``` python
await parser.file_manager_setting('output.csv', 'w')
```
This setting will create a new file (**overwrite the existing one**) named output.csv. This syntax is similar to calling a built-in function [open()](https://docs.python.org/3/library/functions.html#open). 
If you need to continue writing data to an existing file, and at the same time, do not delete the entries in it, you must pass the character `a` as the mode of operation:
``` python
await parser.file_manager_setting('output.csv', 'a')
```
By default, after a successfully processed page, the program saves the current progress to the checkpoint.json file. This is necessary so that in the event of an interrupted data collection process, you can continue from the last successfully processed page.
If you need to assign a different name to the checkpoint file, pass the new file name as the third argument (checkpoint_file_name) to the `parser.file_manager_setting()` method. 
``` python
await parser.file_manager_setting('output.csv', 'a', 'my_point.json')
```
If there is no need to save the checkpoint, pass the constant `None`.
``` python
await parser.file_manager_setting('output.csv', 'a', None)
```
### Progress manager
To generate data scraping tasks, you need to call the configure_progress_manager() method of the Parser class:
``` python
await parser.progress_manager_setting()
```
If no arguments were passed when calling the method, the parser will request data from the server about the number of pages with video games for each category of releases, in this case, **all pages** of the page **of each release category** will be subject to scraping. If you want to get data for only some release categories, you must pass a list of the categories of interest as the releases argument. For example, if you call the configure_progress_manager() method with the following argument, the parser will get data from **all pages** for the **main** and **dlc** release categories:
``` python
await parser.progress_manager_setting(releases=['main', 'dlc'])
```
Also, you can pass only one release category as an argument:
``` python
await parser.progress_manager_setting(releases='main')
```
If you need to get data not from all pages, but only from pages in a certain range, you must pass the appropriate argument to the configure_progress_manager() method. For example, if you call the configure_progress_manager() method with the following argument, the parser will get data from pages 1 to 25 for each release category:
``` python
await parser.progress_manager_setting(pages=[1, 25])
```
If you need to get data from a specific page to the last existing one, you need to pass a list with the constant None as the 2nd element. In such a case, the parser will make a request to the server to get the last page number for the particular release category: 
``` python
await parser.progress_manager_setting(pages=[1, None])
```
You can pass the releases and pages arguments at the same time to the configure_progress_manager() method. In the following example, video game data will be retrieved for the **main** and **dlc** release categories on pages **1 to 50** and **10 to 20**, respectively:
``` python
await parser.progress_manager_setting(releases=['main', 'dlc'], pages=[[1, 50], [10, 20]])
```
If a list with several release categories is passed as the releases argument, and only one list with a range of pages is passed as the pages argument, then this range will be used **for each** release category:
``` python
await parser.progress_manager_setting(releases=['main', 'dlc'], pages=[1, 50])
```
Also, when passing the releases and pages arguments at the same time, you can use the None constant for page ranges, **selectively**:
``` python
await parser.progress_manager_setting(releases=['main', 'dlc'], pages=[[1, 50], [10, None]])
```
### Network manager
To configure the network manager, call the configure_network_manager method of the Parser class and pass one argument to it - the delay range:
``` python
await parser.network_manager_setting((15, 20))
```  
This method will pass to the network manager, which in turn will pass to the delay manager, a range of integers that will be used when generating a **random delay** before sending a request to the server. This approach is necessary in order not to exceed the request limit, otherwise the server will return responses with a status of **429**. It makes sense to reduce the delay range when using a proxy.

[Project information](../../README.md)