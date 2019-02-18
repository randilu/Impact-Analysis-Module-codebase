import boto3

try:
        csv_buffer = StringIO()
        out_df.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        s3_resource.Object('pythonpackages-3.6', 'all_forecasts.csv').put(Body=csv_buffer.getvalue())
        print('Uploaded')
        response = {
            "statusCode": 200,
            "body": "Forecasts successfully uploaded to S3"
        }
        return response
    except BaseException as e:
        print('Upload error')
        print(str(e))
        response = {
            "statusCode": 500,
            "body": "Upload failed"
        }