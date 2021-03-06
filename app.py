from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import boto3
from config import S3_KEY, S3_SECRET_ACESS_KEY, S3_BUCKET
from filters import file_type, datetimeformat


s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET_ACESS_KEY,
)

app = Flask(__name__)
Bootstrap(app)
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/files')
def files():
    s3_resource= boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries= my_bucket.objects.all()
    return render_template('files.html', my_bucket=my_bucket, files=summaries, bucket_name=S3_BUCKET)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(file.filename).put(Body=file)
    return redirect(url_for('files'))


if __name__ == '__main__':
    app.run()
