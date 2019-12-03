"""
This is the job module and supports all the REST actions for the
job data
"""
import os
from werkzeug.utils import secure_filename
from flask import make_response, abort, request
from config import db, app
from harvest.extract_download import *
from models import File, FileSchema
file_path = "{}/storage".format(os.getcwd())


def read_all():
    """
    This function responds to a request for /harvestlog
    with the complete lists of FILES
    :return:        json string of list of files
    """

    # Create the list of job from our data
    file = File.query.order_by(File.id).all()

    # Serialize the data for the response
    file_schema = FileSchema(many=True)
    data = file_schema.dump(file)
    return data


def read_sha1(sha1):
    # Get the job requested
    file = File.query.filter(File.sha1 == sha1).one_or_none()

    # Did we find a job?
    if file is not None:

        # Serialize the data for the response
        file_schema = FileSchema()
        data = file_schema.dump(file)
        return data

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "File not found for SHA1: {sha1}".format(sha1=sha1),
        )


def read_md5(md5):
    # Get the job requested
    file = File.query.filter(File.md5 == md5).one_or_none()

    # Did we find a job?
    if file is not None:

        # Serialize the data for the response
        file_schema = FileSchema()
        data = file_schema.dump(file)
        return data

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "File not found for MD5: {md5}".format(md5=md5),
        )


def delete_sha1(sha1):
    # Get the job requested
    file = File.query.filter(File.sha1 == sha1).one_or_none()

    # Did we find a job_id?
    if file is not None:
        file_schema = FileSchema()
        data = file_schema.dump(file)
        delete_file(data)
        db.session.delete(file)
        db.session.commit()
        return make_response(
            "Deleted {filename}".format(filename=data['filename']), 200,
        )

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "File not found for SHA1: {sha1}".format(sha1=sha1),
        )


def delete_md5(md5):
    # Get the job requested
    file = File.query.filter(File.md5 == md5).one_or_none()

    # Did we find a job_id?
    if file is not None:
        file_schema = FileSchema()
        data = file_schema.dump(file)
        delete_file(data)
        db.session.delete(file)
        db.session.commit()
        return make_response(
            "Deleted {filename}".format(filename=data['filename']), 200,
        )

    # Otherwise, nope, didn't find that job
    else:
        abort(
            404,
            "File not found for MD5: {md5}".format(md5=md5),
        )


def update_sha1(sha1, file):
    update_file = File.query.filter(File.sha1 == sha1).one_or_none()

    if update_file is not None:
        schema = FileSchema()
        upd = schema.load(file, session=db.session)
        upd.sha1 = update_file.sha1

        db.session.merge(upd)
        db.session.commit()
        data = schema.dump(update_file)
        return data, 200

    else:
        abort(404, "File not found for SHA1: {sha1}".format(sha1=sha1))


def update_md5(md5, file):
    update_file = File.query.filter(
        File.md5 == md5
    ).one_or_none()

    if update_file is not None:
        schema = FileSchema()
        upd = schema.load(file, session=db.session)
        upd.md5 = update_file.md5

        db.session.merge(upd)
        db.session.commit()
        data = schema.dump(update_file)

        return data, 200
    else:
        abort(404, f"File not found for MD5 has: {md5}")


def create(file):

    sha1 = file.get("sha1")
    md5 = file.get("md5")
    filename = file.get("filename")

    existing_file = (
        File.query.filter(File.sha1 == sha1)
        .filter(File.md5 == md5)
        .filter(File.filename == filename)
        .one_or_none()
    )

    if existing_file is None:

        # Create a job instance using the schema and the passed in job
        schema = FileSchema()
        new_file = schema.load(file, session=db.session)

        # Add the job to the database
        db.session.add(new_file)
        db.session.commit()

        # Serialize and return the newly created job in the response
        data = schema.dump(new_file)

        return data, 201


def uploader():
    f = request.files['files']
    filename = secure_filename(f.filename)
    f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(f_path)
    data = extract_metadata(f_path)
    entry = create(data)
    return entry, 200


