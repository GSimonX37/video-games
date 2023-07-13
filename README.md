# Video games
The project is a study of video game data.

## Objective of the project
Collect data about video games from various open sources. Analyze the distribution of data, search for anomalies and patterns. The discovered patterns should be confirmed by statistical tests, but based on which a machine learning model should be built.

## Project stages
<table>
    <caption> </caption>
    <thead>
        <tr>
            <th>Number</th>
            <th>Dataset</th>
            <th>Project stages</th>
            <th>Step tasks</th>
            <th>Libraries used</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align:center">1</td>
            <td rowspan="4"><a href=data/backloggd.md>Data</a> from the site <a href=https://www.backloggd.com>backloggd.com</a></td>
            <td>Data collection</td>
            <td>Using your own written parser program, get data by extracting it from the pages of a web resource.</td>
            <td> 
                <ul>
                    <li>bs4</li>
                    <li>requests</li>
                </ul> 
            </td>
            <td><a href=data/backloggd.csv>Completed</a></td>
        </tr>
        <tr>
            <td style="text-align:center">2</td>
            <td>Exploratory analysis</td>
            <td>Analyze basic data properties, detect common distributions, dependencies and anomalies using visualization tools.</td>
            <td> 
                <ul>
                    <li>ast</li>
                    <li>matplotlib</li>
                    <li>numpy</li>
                    <li>pandas</li>
                    <li>seaborn</li>
                </ul> 
            </td>
            <td><a href=notebooks/backloggd_eda.ipynb>Completed</a></td>
        </tr>
        <tr>
            <td style="text-align:center">3</td>
            <td>Statistical analysis</td>
            <td>The regularities discovered at the stage of exploratory analysis should be confirmed by statistical tests. Evaluate the suitability of the discovered patterns for use in machine learning.</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center"><a href=...>Progress</a></td>
        </tr>
        <tr>
            <td style="text-align:center">4</td>
            <td>Machine learning</td>
            <td>Based on the patterns that are suitable and confirmed at the stage of statistical analysis, build a machine learning model.</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
    </tbody> 
</table>

## Acknowledgment


## Help the project
If you are interested in this project, you can help its development by making a contribution. Any comments and suggestions, as well as interesting data sets or web resources worth paying attention to, can be sent to the mail indicated in the profile header.

## License
You may freely copy, modify and distribute this project or parts of it as you see fit. However, it is correct if you provide a link to this repository in your work.