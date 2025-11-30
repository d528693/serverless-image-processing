# Serverless Image Processing Pipeline

A fully serverless image processing application built with AWS services that automatically resizes uploaded images to thumbnails. The uploaded images are resized to 200x200 pixel that is the thumbnail size.


# AWS Services Used

**Amazon S3** - Stores original and resized images
**AWS Lambda** - Executes image resizing code with Python
**AWS Step Functions** - Orchestrates the workflow
**Amazon API Gateway** - Provides REST API endpoint
**IAM** - Manages permissions and roles

---

## How to Use the Image Resizing Application

This instruction will use PowerShell commands to demonstrate how the application works.

### 1. Open the Windows Powershell and Set-Location to the directory that we will work on.

### 2. Prepare the image to be resized

We can prepare the image and place it in the directory that we will work on.

In this demonstration, the uploaded image is called "test_image01.jpg"

### 3. Upload a Test Image to S3

S3 Bucket Names
- **Source Bucket Name:** `dawich-original-image`
- **Destination Bucket Name:** `dawich-resized-image`

We can upload the image to the bucket by using the following command.
- PowerShell: aws s3 cp test_image01.jpg s3://dawich-original-image/test_image01.jpg
- (The Command Structure: aws s3 cp test_image01.jpg s3://[Source Bucket Name]/test_image01.jpg)

We can verify whether the image is uploaded in the bucket by using the following command.
- PowerShell: aws s3 ls s3://dawich-original-image/
- (The Command Structure: aws s3 ls s3://[Source Bucket Name]/)

### 4. Trigger via API Gateway

We can set up the API by using the following command.
- Powershell: $apiUrl = "https://367mo9jolf.execute-api.ca-central-1.amazonaws.com/prod/process" 
- (The Command Structure: $apiUrl = "YOUR_API_GATEWAY_URL/process")

Then, we create the request body by the following command.
- Powershell:
>$body = @{
>    imageKey = "test_image01.jpg"
>} | ConvertTo-Json

After that, we can now call the API by the following command:
- Powershell: $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json"
- (The Command Structure: $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json")

### 5. Verify Results

Check your destination S3 bucket for the thumbnail using the following command.
- Powershell: aws s3 ls s3://dawich-resized-image/
- (The Command Structure: aws s3 ls s3://[Destination Bucket Name]/)

You should see a file named `thumbnail-test-image01.jpg` in the destination bucket.

---

## How It Works

1. **User triggers the workflow** by calling the API Gateway endpoint with an image key
2. **API Gateway** starts the Step Functions state machine
3. **Step Functions** invokes the Lambda function with the image details
4. **Lambda function**:
   - Downloads the original image from the source S3 bucket
   - Resizes it to a 200x200 thumbnail using Pillow
   - Uploads the thumbnail to the destination S3 bucket



