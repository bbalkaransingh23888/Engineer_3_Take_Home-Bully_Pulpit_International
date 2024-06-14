
# Objective
The goal of this project is to convert this CLI project to a web application that can be run locally. The app should meet the requirements outlined in the assignment section below. You may use any web framework you are comfortable with, but we recommend using Django and React. We don't want you to spend more than a few hours on this project, so please prioritize the requirements and let us know if you run out of time. We know that some of the requirements are vague, so feel free to make assumptions and make your best judgment. We are looking for clean, well-organized code and a good user experience that accomplishes the goals of the assignment.

We have provided a few functions that our team has written to process the raw data, as well as a few sample audience files.

### The Assignment
In each campaign, we define a target audience – likely voters, opinion influencers, etc. – and we want to reach them with the most efficient targeting possible with zipcodes. Our data warehouse contains data on the total population within each zipcode, as well as the number of people in our audience in each zipcode, so we can identify the zipcodes with the best target density and rank zipcodes.
 
However, because zipcodes vary in size and campaigns differ, we want to equip our analysts with a tool that can allow them to understand the tradeoffs at different levels of reach. As we add more zipcodes in, our campaign reaches more of our target audience, but it becomes less efficient.

In the app, a user should be able to:
 - Load the data from a given audience file (see sample files in the `./data` folder)
 - Display key statistics from the audience file, like the ones provided in the `./src/reach_efficiency_by_zipcode.py` file.
 - Chart the efficiency of zipcodes at different reach levels – e.g., how does efficiency decrease as reach increases?
 
### Getting Started
To get started, you need python 3 installed locally, [`pipenv`](https://pipenv.pypa.io/en/latest/installation.html) and [GNU Make](https://www.gnu.org/software/make/). You can install the required packages by running the following command in the root directory of the project:
```bash
    make build
```
> [!TIP]
> We do not want to waste time with the setup. If you have any issues, please let us know, so we can help you get started.

To run the CLI app, you can run the following command:
```bash
    make run <path-to-audience-file>
```

to run the tests, you can run the following command:
```bash
    make test
```