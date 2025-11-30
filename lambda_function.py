"""
AWS Lambda Function: Image Resizer
This function resizes images to thumbnail size (200x200 pixels)
"""

import json
import boto3
import os
from PIL import Image
from io import BytesIO

# Initialize S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Main Lambda handler function
    
    Args:
        event: Contains the source bucket and image key
        context: Lambda context object
        
    Returns:
        Success or error response
    """
    
    try:
        # Extract bucket and key from event
        source_bucket = event.get('sourceBucket')
        image_key = event.get('imageKey')
        destination_bucket = event.get('destinationBucket')
        
        # Validate inputs
        if not source_bucket or not image_key or not destination_bucket:
            raise ValueError("Missing required parameters: sourceBucket, imageKey, or destinationBucket")
        
        print(f"Processing image: {image_key} from bucket: {source_bucket}")
        
        # Download image from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=image_key)
        image_content = response['Body'].read()
        
        # Open image with Pillow
        image = Image.open(BytesIO(image_content))
        
        # Get original dimensions
        original_width, original_height = image.size
        print(f"Original size: {original_width}x{original_height}")
        
        # Resize to thumbnail (200x200, maintaining aspect ratio)
        thumbnail_size = (200, 200)
        image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Get new dimensions
        new_width, new_height = image.size
        print(f"Resized to: {new_width}x{new_height}")
        
        # Save resized image to buffer
        buffer = BytesIO()
        
        # Determine format from original image
        image_format = image.format if image.format else 'JPEG'
        image.save(buffer, format=image_format, quality=85)
        buffer.seek(0)
        
        # Create new key for thumbnail (add 'thumbnail-' prefix)
        thumbnail_key = f"thumbnail-{image_key}"
        
        # Upload resized image to destination bucket
        s3_client.put_object(
            Bucket=destination_bucket,
            Key=thumbnail_key,
            Body=buffer,
            ContentType=response['ContentType']
        )
        
        print(f"Successfully uploaded thumbnail: {thumbnail_key}")
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image resized successfully',
                'originalImage': image_key,
                'thumbnailImage': thumbnail_key,
                'originalSize': f"{original_width}x{original_height}",
                'thumbnailSize': f"{new_width}x{new_height}"
            }),
            'success': True
        }
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        
        # Return error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing image',
                'error': str(e)
            }),
            'success': False
        }
