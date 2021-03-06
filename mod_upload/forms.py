import os

from flask_wtf import Form
from wtforms import FileField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from mod_home.models import CCExtractorVersion
from mod_sample.models import ForbiddenExtension
from mod_upload.models import Platform


class UploadForm(Form):
    accept = '.ts, .txt, .srt, .png, video/*'

    file = FileField('File to upload', [
        DataRequired(message='No file was provided.')
    ], render_kw={'accept': accept})
    submit = SubmitField('Upload file')

    @staticmethod
    def validate_file(form, field):
        # File cannot end with a forbidden extension
        filename, file_extension = os.path.splitext(field.data.filename)
        if len(file_extension) > 0:
            forbidden = ForbiddenExtension.query.filter(
                ForbiddenExtension.extension == file_extension[1:]).first()
            if forbidden is not None:
                raise ValidationError('Extension not allowed')


class DeleteQueuedSampleForm(Form):
    submit = SubmitField('Delete queued file')


class CommonSampleForm(Form):
    notes = TextAreaField(
        'Notes', [DataRequired(message='Notes are not filled in')])
    parameters = TextAreaField(
        'Parameters', [DataRequired(message='Parameters are not filled in')])
    platform = SelectField(
        'Platform', [DataRequired(message='Platform is not selected')],
        coerce=str, choices=[(p.value, p.description) for p in Platform])
    version = SelectField(
        'Version', [DataRequired(message='Version is not selected')],
        coerce=int)

    @staticmethod
    def validate_version(form, field):
        v = CCExtractorVersion.query.filter(
            CCExtractorVersion.id == field.data).first()
        if v is None:
            raise ValidationError('Invalid version selected')


class FinishQueuedSampleForm(CommonSampleForm):
    submit = SubmitField('Finalize sample')
