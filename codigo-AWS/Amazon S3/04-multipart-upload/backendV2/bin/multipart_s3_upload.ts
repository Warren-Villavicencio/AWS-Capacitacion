#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { MultipartS3UploadStack } from '../lib/multipart_s3_upload-stack';

const app = new cdk.App({});
new MultipartS3UploadStack(app, 'MultipartS3UploadStack', {
    env: { 
        account: '', // Tu ID de cuenta de AWS
        region: '', // La región de AWS que prefieras
    },
});
