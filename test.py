#!/usr/bin/env python3
import os
import sys
import jarboto

def main():
    if len(sys.argv) < 3:
        print("Usage: {} <bucket> <file-to-upload>".format(sys.argv[0]))
        sys.exit(1)

    bucket = sys.argv[1]
    file_path = sys.argv[2]

    # Set mandatory environment variables (except bucket, which is provided via an argument)
    os.environ['JARVICE_S3_BUCKET'] = bucket
    if 'JARVICE_S3_ACCESSKEY' not in os.environ or 'JARVICE_S3_SECRETKEY' not in os.environ:
        print("Please set JARVICE_S3_ACCESSKEY and JARVICE_S3_SECRETKEY in your environment.")
        sys.exit(1)
    if 'JARVICE_S3_ENDPOINTURL' not in os.environ:
        print("Please set JARVICE_S3_ENDPOINTURL in your environment. Normally https://storage.googleapis.com")
        sys.exit(1)

    # Create an S3 instance using jarboto
    try:
        s3 = jarboto.S3()
    except jarboto.ConfigError as e:
        print("Configuration Error:", e)
        sys.exit(1)

    # Read the file to upload
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except IOError as e:
        print("File read error:", e)
        sys.exit(1)

    # Use the file name as the S3 object name
    object_name = os.path.basename(file_path)

    # Upload the file to S3 using the put method
    try:
        s3.put(object_name, content)
        print(f"Successfully uploaded '{file_path}' to bucket '{bucket}' as '{object_name}'")
    except jarboto.S3Error as e:
        print("S3Error during upload:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()