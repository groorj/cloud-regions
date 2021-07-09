# cloud-regions

## Table of Contents
- [What does it do ?](https://github.com/groorj/cloud-regions#what-does-it-do)
- [This project uses](https://github.com/groorj/cloud-regions#this-project-uses)
- [Where does the information comes from](https://github.com/groorj/cloud-regions#where-does-the-information-comes-from)
- [Get started](https://github.com/groorj/cloud-regions#get-started)
- [Clean up](https://github.com/groorj/cloud-regions#clean-up)
- [Notes](https://github.com/groorj/cloud-regions#notes)

## What does it do

If you ever needed to find AWS regions and avaliability zones information, this project might help you.

It uses AWS API Gateway to provide you with an REST API to query region information. You can use this code to deploy your own API and integrate with your applications.

## This project uses

- The [Serverless Framework](https://www.serverless.com/)
- [AWS API Gateway](https://aws.amazon.com/api-gateway/)
- Python3
- Serverless plugins
  - serverless-python-requirements
  - serverless-offline

## Where does the information comes from

A JSON file with the information is populated manually. 

The first version came from this repo: https://raw.githubusercontent.com/jsonmaur/aws-regions/master/regions.json

You can find the file used by this project here:

[https://github.com/groorj/cloud-regions/blob/main/aws-regions.json](https://github.com/groorj/cloud-regions/blob/main/aws-regions.json)

An example of how the file looks like:

```json
    {
      "name": "N. Virginia",
      "full_name": "US East (N. Virginia)",
      "code": "us-east-1",
      "public": true,
      "government_cloud": false,
      "launched": "2006",
      "country_name": "United States of America",
      "country_code": "USA",
      "geographic_location": "North America",
      "zones": [
        "us-east-1a",
        "us-east-1b",
        "us-east-1c",
        "us-east-1d",
        "us-east-1e",
        "us-east-1f"
      ]
    },
```

## Get started

- Install the Serveless Framework
- Install the serverless-python-requirements plugin

```bash
sls plugin install -n serverless-python-requirements
```

- Install the serverless-offline plugin so you can test locally

```bash
sls plugin install -n serverless-offline
```

- Deploy the serverless architecture by running:

```bash
serverless deploy --aws-profile <YOUR_PROFILE_NAME>
```

Replace <YOUR_PROFILE_NAME> with your [AWS profile name](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).

If the deployment is successful, you will see the API Gateway endpoints created:

```text
  GET - https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/health/check
  GET - https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/region/{region_code}/info
  GET - https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/regions/info
```

## How to use it

### Get information for one specific region
```bash
curl -vvvv https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/region/sa-east-1/info
```

**Result:**
```json
{
  "request": {
    "request_status": "Success"
  },
  "info": {
    "cloud_provider": "AWS",
    "cloud_provider_name": "Amazon Web Services",
    "github_repo": "https://github.com/groorj/cloud-regions",
    "file_last_modified": "Thu  8 Jul 2021 16:20:40 EDT"
  },
  "data": {
    "name": "São Paulo",
    "full_name": "South America (São Paulo)",
    "code": "sa-east-1",
    "public": true,
    "government_cloud": false,
    "launched": "2011",
    "country_name": "Brazil",
    "country_code": "BRA",
    "geographic_location": "South America",
    "zone_limit": 2,
    "zones": [
      "sa-east-1a",
      "sa-east-1b",
      "sa-east-1c"
    ]
  }
}
```

Under "request" you will find "request_status" that can be "Success" or "Fail".

Here is an example of a fail (wrong region):

```bash
curl -vvvv https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/region/sa-test-1000/info
```

**Result:**
```json
{
  "request": {
    "request_status": "Fail",
    "error_message": "Region code NOT found.",
    "http_error_code": 404
  }
}
```

And the HTTP header:
```http
* Server certificate:
*  subject: CN=*.execute-api.us-east-2.amazonaws.com
*  start date: Jun 30 00:00:00 2021 GMT
*  expire date: Jul 29 23:59:59 2022 GMT
*  subjectAltName: host "xs54oom6k7.execute-api.us-east-2.amazonaws.com" matched cert's "*.execute-api.us-east-2.amazonaws.com"
*  issuer: C=US; O=Amazon; OU=Server CA 1B; CN=Amazon
*  SSL certificate verify ok.
* Using HTTP2, server supports multi-use
* Connection state changed (HTTP/2 confirmed)
* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
* Using Stream ID: 1 (easy handle 0x15c80d600)
> GET /prod/region/sa-test-1000/info HTTP/2
> Host: xs54oom6k7.execute-api.us-east-2.amazonaws.com
> User-Agent: curl/7.64.1
> Accept: */*
>
* Connection state changed (MAX_CONCURRENT_STREAMS == 128)!
< HTTP/2 404
< content-type: application/json
< content-length: 82
< date: Fri, 09 Jul 2021 15:37:01 GMT
< x-amzn-requestid: 247705cc-447a-4a99-98a9-69d4f324b0a5
< access-control-allow-origin: *
< x-amz-apigw-id: CNX8sHqvCYcFU0A=
< x-amzn-trace-id: Root=1-60e86d1d-129f0614431d2ac6645a6fdd;Sampled=0
< x-cache: Error from cloudfront
< via: 1.1 ac1cb1fdb7cf3984f94f9f190169eb3a.cloudfront.net (CloudFront)
< x-amz-cf-pop: YUL62-C2
< x-amz-cf-id: vcMy8Gr0Bp-zBUeUT6zohSHmF5eCSiuGn4k9ha2KYJ5jTMYhPa6lYA==
```

### Get information for all regions
```bash
curl -vvvv https://xs54oom6k7.execute-api.us-east-2.amazonaws.com/prod/regions/info
```

**Result:**
```json
{
{
  "request": {
    "request_status": "Success"
  },
  "info": {
    "cloud_provider": "AWS",
    "cloud_provider_name": "Amazon Web Services",
    "github_repo": "https://github.com/groorj/cloud-regions",
    "file_last_modified": "Thu  8 Jul 2021 16:20:40 EDT"
  },
  "data": [
    {
      "name": "N. Virginia",
      "full_name": "US East (N. Virginia)",
      "code": "us-east-1",
      "public": true,
      "government_cloud": false,
      "launched": "2006",
      "country_name": "United States of America",
      "country_code": "USA",
      "geographic_location": "North America",
      "zones": [
        "us-east-1a",
        "us-east-1b",
        "us-east-1c",
        "us-east-1d",
        "us-east-1e",
        "us-east-1f"
      ]
    },
(...)
  ]
}
```

## Clean up

- Destroy the serverless architecture by running:

```bash
serverless remove --aws-profile <YOUR_PROFILE_NAME>
```

## Notes
Running this code will create AWS resources in your account that might not be included in the free tier. I am not responsable for anything you do with this code. Use it at your own risk.