# Video games
The project is a study of video game data.

## Objective of the project
Collect data about video games from various open sources. Analyze the distribution of data, search for anomalies and patterns. The discovered patterns should be confirmed by statistical tests, but based on which a machine learning model should be built.

## Project stages
<table>
    <caption><b>Stages of the project with their content and results</b></caption>
    <thead>
        <tr>
            <th>№</th>
            <th>Dataset</th>
            <th>Project stages</th>
            <th>Brief description of results</th>
            <th>Libraries used</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align:center">1</td>
            <td style="text-align:center" rowspan="4"><a href=data/backloggd/README.md>Data</a> from the site <br> <a href=https://www.backloggd.com>backloggd.com</a></td>
            <td>Data collection</td>
            <td>Using your own written <a href=parsers/backloggd/README.md>parser program</a>, get data by extracting it from the pages of a web resource.</td>
            <td> 
                <ul>
                    <li>aiohttp</li>
                    <li>requests</li>
                </ul> 
            </td>
            <td><a href=data/backloggd/backloggd.csv>Updated</a></td>
        </tr>
        <tr>
            <td style="text-align:center">2</td>
            <td>Exploratory analysis</td>
            <td>
                <ol>
                    <li>The distributions of the main variables are analyzed.</li>
                    <li>The analysis of the distribution of the rating of video games by:
                        <ul>
                            <li>video game genres;</li>
                            <li>developers;</li>
                            <li>gaming platforms.</li>
                        </ul>
                    </li>
                    <li>The dependence of the number of video game players was found.</li>
                </ol> 
            </td>
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
            <td>
                <ol>
                    <li>Statistical tests were carried out to compare the average ratings of video games for samples with different:</li>
                        <ul>
                            <li>video game genres (ANOVA, Tukey's post hoc test);</li>
                            <li>developers (ANOVA, Tukey's post hoc test, Student's t-test);</li>
                            <li>gaming platforms (ANOVA, Tukey's post hoc test).</li>
                        </ul>
                    </li>
                </ol> 
            </td>
            <td> 
                <ul>
                    <li>matplotlib</li>
                    <li>numpy</li>
                    <li>pandas</li>
                    <li>seaborn</li>
                    <li>scipy</li>
                </ul> 
            </td>
            <td style="text-align:center"><a href=notebooks/backloggd_sda.ipynb>Progress</a></td>
        </tr>
        <tr>
            <td style="text-align:center">4</td>
            <td>Machine learning</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
    </tbody> 
</table>

<br>

<table>
    <caption><b>Description of the main stages of the project</b></caption>
    <thead>
        <tr>
            <th>Stage name</th>
            <th>Stage description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data collection</td>
            <td>Using your own written parser program, get data by extracting it from the pages of a web resource.</td>
        </tr>
        <tr>
            <td>Exploratory analysis</td>
            <td>Analysis of the main properties of data and distributions, search for dependencies and anomalies using visualization tools.</td>
        </tr>
        <tr>
            <td>Statistical analysis</td>
            <td>The regularities discovered at the stage of exploratory analysis should be confirmed by statistical tests. Evaluate the suitability of the discovered patterns for use in machine learning.</td>
        </tr>
        <tr>
            <td>Machine learning</td>
            <td>Based on the patterns that are suitable and confirmed at the stage of statistical analysis, build a machine learning model.</td>
        </tr>
    </tbody>     
</table>

## Thanks
I would like to express my gratitude to [Irina Romanovsky](https://www.linkedin.com/in/irina-romanovsky-034338143/) ([GitHub](https://github.com/needsomecats)) for her help and support in creating this project.


## Help the project
If you are interested in this project, you can help its development by making a contribution. Any comments and suggestions, as well as interesting data sets or web resources worth paying attention to, can be sent to the mail indicated in the profile header.

## License
You may freely copy, modify and distribute this project or parts of it as you see fit. However, it is correct if you provide a link to this repository in your work.