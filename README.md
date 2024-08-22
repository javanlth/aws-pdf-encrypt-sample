# aws-pdf-encrypt-sample

This is an attempt at generating CI/CD pipelines with the help of AWS SAM for the deployment of a PDFEncrypt Lambda function (the code for this function itself is a sample code provided by AWS at [https://docs.aws.amazon.com/lambda/latest/dg/file-processing-app.html](https://docs.aws.amazon.com/lambda/latest/dg/file-processing-app.html)).

This function takes in any PDF file with name format \<name>.pdf that has been uploaded to a source S3 bucket and then outputs a password-encrypted file with name format \<name>-encrypted.pdf. Password has been pre-defined in AWS secret manager, which is then retrieved by the lambda function.

## Setting this up

To be able to set this pipeline up for your use in your own repository, you will need to do the following:

### 1. Make a clone of this repository in your desired directory.

'''
git clone https://github.com/javanlth/aws-pdf-encrypt-sample.git
'''

### 2. Have both the AWS CLI and the AWS SAM CLI installed.
This presumes that you have already signed up for an AWS account and created an administrative IAM user.

To install the AWS CLI, refer to instructions at [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Briefly, if you are installing it on a bash shell, you would run the following commands:

```
sudo yum remove awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Next, to configure your security credentials for AWS CLI, refer to  [https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html). Briefly, run the below command and follow the prompts for inputs.

```
aws configure sso
```

While configuring your security credentials, take note of your account ID and save it as the repository secret AWS_ACCOUNT_ID.

Finally, to install AWS SAM CLI, follow the instructions on [https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

### 3. Obtaining the ARNs and storing them as Github Repository Secrets.
To obtain the various ARNs that will be needed for deploying the CI/CD pipeline, run the following AWS SAM commands:

```
sam pipeline bootstrap --stage dev
sam pipeline bootstrap --stage prod
```

For each line of command, you will be guided through a series of prompts like this:

```
We will ask for [1] stage definition, [2] account details, and
[3] references to existing resources in order to bootstrap these pipeline resources.

[1] Stage definition
Stage configuration name: dev

[2] Account details
The following AWS credential sources are available to use.
To know more about configuration AWS credentials, visit the link below:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
        1 - Environment variables (not available)
        2 - <your named profile> (named profile)

        q - Quit and configure AWS credentials
Select a credential source to associate with this stage: 2
Associated account <your account ID> with configuration test.

Enter the region in which you want these resources to be created [us-east-1]: <region of your choice>
Select a user permissions provider:
        1 - IAM (default)
        2 - OpenID Connect (OIDC)
Choice (1, 2): 2
Select an OIDC provider:
        1 - GitHub Actions
        2 - GitLab
        3 - Bitbucket
Choice (1, 2, 3): 1
Enter the URL of the OIDC provider [https://token.actions.githubusercontent.com]:
Enter the OIDC client ID (sometimes called audience) [sts.amazonaws.com]:
Enter the GitHub organization that the code repository belongs to. If there is no organization enter your username instead: <your GitHub username>
Enter GitHub repository name: aws-pdf-encrypt-sample
Enter the name of the branch that deployments will occur from [main]:

[3] Reference application build resources
Enter the pipeline execution role ARN if you have previously created one, or we will create one for you []:
Enter the CloudFormation execution role ARN if you have previously created one, or we will create one for you []:
Please enter the artifact bucket ARN for your Lambda function. If you do not have a bucket, we will create one for you []:
Does your application contain any IMAGE type Lambda functions? [y/N]: Y
'''

Once bootstrapping is complete, navigate to .aws-sam/pipeline and open the pipelineconfig.toml file. Here you will find the ARNs that AWS SAM has configured for you.

```
[dev.pipeline_bootstrap.parameters]
pipeline_execution_role = "arn:aws:iam::<your account ID>:role/aws-sam-cli-managed-dev-pipel-PipelineExecutionRole-<some UID>"
cloudformation_execution_role = "arn:aws:iam::<your account ID>:role/aws-sam-cli-managed-dev-p-CloudFormationExecutionRo-<some UID>"
artifacts_bucket = "aws-sam-cli-managed-dev-pipeline-r-artifactsbucket-<some UID>"
image_repository = "<your account ID>.dkr.ecr.ap-northeast-1.amazonaws.com/aws-sam-cli-managed-dev-pipeline-resources-imagerepository-<some UID>"
region = "ap-northeast-1"

[prod.pipeline_bootstrap.parameters]
pipeline_execution_role = "arn:aws:iam::<your account ID>:role/aws-sam-cli-managed-prod-pipe-PipelineExecutionRole-<some UID>"
cloudformation_execution_role = "arn:aws:iam::<your account ID>:role/aws-sam-cli-managed-prod--CloudFormationExecutionRo-<some UID>"
artifacts_bucket = "aws-sam-cli-managed-prod-pipeline--artifactsbucket-<some UID>"
image_repository = "<your account ID>.dkr.ecr.ap-northeast-1.amazonaws.com/aws-sam-cli-managed-prod-pipeline-resources-imagerepository-<some UID>"
region = "ap-northeast-1"
```

These parameter values will be saved in your GitHub repository secrets for the workflow files to refer to later.

Copy the values from the files (omitting the "") and save them as the following secrets accordingly: (left: parameters in pipelineconfig.toml file, right: name of secrets variable)
From [dev.pipeline_bootstrap.parameters]
pipeline_execution_role (only the part after role/) --> TESTING_PIPELINE_EXECUTION_ROLE_NAME
cloudformation_execution_role --> TESTING_CLOUDFORMATION_EXECUTION_ROLE
artifacts_bucket --> TESTING_ARTIFACTS_BUCKET
image_repository --> TESTING_IMAGE_REPOSITORY


From [prod.pipeline_bootstrap.parameters]
pipeline_execution_role (only the part after role/) --> PROD_PIPELINE_EXECUTION_ROLE_NAME
cloudformation_execution_role --> PROD_CLOUDFORMATION_EXECUTION_ROLE
artifacts_bucket --> PROD_ARTIFACTS_BUCKET
image_repository --> PROD_IMAGE_REPOSITORY

## Automated tests

### Unit testing
During the unit testing stage, the pipeline will run the pdf_encrypt function locally to ensure that the file can be successfully encrypted.

The pipeline will only proceed to the deployment stage when this test has been passed.

### Deployment stage testing
During the deployment stage, the pipeline will check the following:
1. The source S3 bucket is created.
2. The Lambda function is invoked upon uploading a file to the source s3 bucket.
3. The encrypted PDF can be downloaded from the destination bucket.

Any errors detected during this stage could be due to insufficient access permissions for the execution role.

## Using it

Once the Lambda function has been successfully deployed onto the production stage of AWS, you may upload any PDF to the source S3 bucket by running the following command:

```
aws s3api put-object --bucket <NAME-OF-SOURCEBUCKET> --key <PDF-NAME>.pdf --body ./<PDF-NAME>.pdf
```

The Lambda function has been configured to automatically run and encrypt the uploaded PDF, then upload the encrypted PDF into the destination S3 bucket. You may then download the encrypted PDF from the destination S3 bucket with the following command.

```
aws s3api get-object --bucket <NAME-OF-SOURCEBUCKET>-encrypted --key <PDF-NAME>_encrypted.pdf <PDF-NAME>_encrypted.pdf
```

The encrypted file will have the _encrypted suffix in its name. When you open it, you should be prompted to enter a password, which will be the one you have configured in your AWS secrets manager.

