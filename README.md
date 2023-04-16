
# Working Days

An application which lists all of the working days in a selected month in England, taking into account weekends and public holidays.
## Features

- Month and year selector
- Public holidays sourced from the GOV.UK bank holiday API https://www.api.gov.uk/gds/bank-holidays/#bank-holidays
- List of working days
- Responsive


## Authors

- Steven Diffey - [@stiffey](https://github.com/Stiffey)


## Demo

https://workingdays.forestrun.dev/


## Run Locally

Clone the project

```bash
  git clone https://github.com/Stiffey/working-days.git
```

Go to the project directory

```bash
  cd working-days
```


Setup a local virtual server
```bash
   python -m venv venv
```

Activate the virtual server
```bash
   source venv/bin/activate
```

Install dependencies
```bash
  pip install requirements.txt 
```

Start the server

```bash
  flask --app app --debug run
```


## Deployment

A Docker file is included so you can run it locally or on a cloud server.


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](http://stevendiffey.co.uk/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/stevendiffey/)

