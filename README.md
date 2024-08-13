# aws-pdf-encrypt-sample

This is an attempt at generating CI/CD pipelines with the help of AWS SAM for the deployment of a PDFEncrypt Lambda function.

This function takes in any PDF file with name format <name>.pdf that has been uploaded to a source S3 bucket and then outputs a password-encrypted file with name format <name>-encrypted.pdf. Password has been pre-defined in AWS secret manager, which is then retrieved by the lambda function.