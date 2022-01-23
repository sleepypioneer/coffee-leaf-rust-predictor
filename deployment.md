# Deployment Notes

## AWS LAMBDA

I deployed the AWS Lambda by first pushing the Docker image built locally to the AWS Elast Container Registry. 


## AWS API GATEWAY

The API Gateway allows incoming requests to invoke the Lambda function. One endpoint `/coffee-leaf-rust-prediction` takes post requests. The URL for an image is passed as a URL parameter which then is available in the event object of the lambda function. To do this I had to set up a custom mapping which looked like this:

```
#set($inputRoot = $input.path('$'))
{
  "url" : "$input.params('url')"
}
```

Currently I set the Gateway to not have any authorisation, I may change this is I suspect the endpoint is being abused.

*NOTE* When running locally there is no API Gateway in front of the Lambda function so the URL has to be passed in the body of the request.

## STREAMLIT APP

The front end app is deployed on the streamlit servers. To do so it requires the use of streamlit secrets to pass through the correct URL for the LAMBDA URL. The local version requires on environment variables for this, so I set an ENV variable to know which environment is expected.