#pytest script to check encrypt_pdf function

import boto3
import json
import pytest
import time
import os
from ../lambda_function import encrypt_pdf

source_bucket_name = 'mocho'
dest_bucket_name = source_bucket_name + '-encrypted'

@pytest.fixture
def file_path_to_encrypt():
    file_name = 'test.pdf'
    file_path = os.path.join(os.path.dirname(__file__), "../", file_name)
    return file_path
    

@pytest.mark.order(1)
def test_encrypt_working(file_path_to_encrypt):
    file_encrypted = False
    try:
        encrypt_pdf(file_path_to_encrypt, "encrypted.pdf", "test")
        file_encrypted = True
    except:
        print("Error: could not encrypt file")

    assert file_encrypted, "Could not encrypt file"


def test_cleanup(cleanup):
    # This test uses the cleanup fixture and will be executed last
    pass
