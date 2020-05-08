# lamba-mongo-health-check
Lamba to check the health of a Mongo database

## Development

### Contributions
Contributions are welcome.

### Requirements
Run `pipenv install --dev` to install both production and development
requirements, and `pipenv shell` to activate the virtual environment. For more
information see the [pipenv docs](https://pipenv.pypa.io/en/latest/).

After activating the virtual environment, run `pre-commit install` to install
the [pre-commit](https://pre-commit.com/) git hook.

### Create a local build

```shell script
$ sam build --use-container
```

### Run locally

```shell script
$ sam local invoke HelloWorldFunction --event events/event.json
```

### Run unit tests
Tests are defined in the `tests` folder in this project. Use PIP to install the
[pytest](https://docs.pytest.org/en/latest/) and run unit tests.

```shell script
$ python -m pytest tests/ -v
```

## Deployment

### Build

```shell script
sam build
```

## Deploy Lambda to S3
This requires the correct permissions to upload to bucket
`bootstrap-awss3cloudformationbucket-19qromfd235z9` and
`essentials-awss3lambdaartifactsbucket-x29ftznj6pqw`

```shell script
sam package --template-file .aws-sam/build/template.yaml \
  --s3-bucket essentials-awss3lambdaartifactsbucket-x29ftznj6pqw \
  --output-template-file .aws-sam/build/lamba-mongo-health-check.yaml

aws s3 cp .aws-sam/build/lamba-mongo-health-check.yaml s3://bootstrap-awss3cloudformationbucket-19qromfd235z9/lamba-mongo-health-check/master/
```

## Install Lambda into AWS
Create the following [sceptre](https://github.com/Sceptre/sceptre) file

config/prod/lamba-mongo-health-check.yaml
```yaml
template_path: "remote/lamba-mongo-health-check.yaml"
stack_name: "lamba-mongo-health-check"
stack_tags:
  Department: "Platform"
  Project: "Infrastructure"
  OwnerEmail: "it@sagebase.org"
hooks:
  before_launch:
    - !cmd "curl https://s3.amazonaws.com/bootstrap-awss3cloudformationbucket-19qromfd235z9/lamba-mongo-health-check/master/lamba-mongo-health-check.yaml --create-dirs -o templates/remote/lamba-mongo-health-check.yaml"
```

Install the lambda using sceptre:
```shell script
sceptre --var "profile=my-profile" --var "region=us-east-1" launch prod/lamba-mongo-health-check.yaml
```

## Author

Your Name Here.
