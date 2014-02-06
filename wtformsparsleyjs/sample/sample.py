__author__ = 'Johannes Gehrs (jgehrs@gmail.com)'

from flask import Flask, render_template, request
from wtforms import Form, validators
from wtformsparsleyjs import IntegerField, BooleanField, SelectField, StringField

app = Flask(__name__)


@app.route('/parsley_testform', methods=['GET', 'POST'])
def parsley_testform():
    form = ParsleyTestForm(request.form)
    if request.method == 'POST': form.validate()
    return render_template('wtforms_parsley_sample.html', form=form)


class ParsleyTestForm(Form):
    email = StringField('E-Mail Address', [
        validators.Email('Sorrry, not a valid email address.')
    ], default='test@example.com')
    first_value = StringField('Some Value', default='Some value')
    second_value = StringField('Should be identical', [
        validators.EqualTo(message='Sorry, values do not match.',
                           fieldname='first_value')
    ], default='Some value')
    ip_address = StringField('IP4 Address', [
        validators.IPAddress(message='Sorry, not a valid IP4 Address.')
    ], default='127.0.0.1')
    string_length = StringField('Length of String (5 to 10)', [
        validators.Length(message='Length should be between 5 and 10 characters.',
                          min=5, max=10)
    ], default='Hello!')
    number_range = IntegerField('Number Range (5 to 10)', [
        validators.NumberRange(message='Range should be between 5 and 10.',
                               min=5, max=10)
    ], default=7)

    required_text = StringField('Required Field', [
        validators.DataRequired(message='Sorry, this is a required field.')
    ], default='Mandatory text')
    required_select = SelectField('Required Select', [
        validators.DataRequired(
            message='Sorry, you have to make a choice.')
    ], choices=[('', 'Please select an option'), ('cpp', 'C++'), ('py', 'Python'),
                ('text', 'Plain Text')
    ], default='py')
    required_checkbox = BooleanField('Required Checkbox', [
        validators.DataRequired(message='Sorry, you need to accept this.')
    ], default=True)
    regexp = StringField('Regex-Matched Hex Color-Code', [
        validators.Regexp(message='Not a proper color code, sorry.',
                          regex=r'^#[A-Fa-f0-9]{6}$')
    ], default='#7D384F')
    url = StringField('URL Field', [
        validators.URL(message='Sorry, this is not a valid URL,')
    ], default='http://example.com/parsley')
    anyof = StringField('Car, Bike or Plane?', [
        validators.AnyOf(message='Sorry, you can only choose from car, bike and plane',
                         values=['car', 'bike', 'plane'])
    ], default='car')
