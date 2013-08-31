__author__ = 'Johannes Gehrs (jgehrs@gmail.com)'

import re
import copy

from wtforms.validators import Length, NumberRange, Email, EqualTo, IPAddress, \
    Required, Regexp, URL, AnyOf
from wtforms import TextField
from wtforms.widgets import TextInput as _TextInput, PasswordInput as _PasswordInput, \
    CheckboxInput as _CheckboxInput, Select as _Select, Input
from wtforms.fields import TextField as _TextField, BooleanField as _BooleanField, \
    DecimalField as _DecimalField, IntegerField as _IntegerField, \
    FloatField as _FloatField, PasswordField as _PasswordField, \
    SelectField as _SelectField


def parsley_kwargs(field, kwargs):
    """
    Return new *kwargs* for *widget*.

    Generate *kwargs* from the validators present for the field.

    Note that the regex validation relies on the regex pattern being compatible with
    both ECMA script and Python. The regex is not converted in any way.
    It's possible to simply supply your own "data-regexp" keyword to the field
    to explicitly provide the ECMA script regex.
    See http://flask.pocoo.org/docs/patterns/wtforms/#forms-in-templates

    Note that the WTForms url vaidator probably is a bit more liberal than the parsley
    one. Do check if the behaviour suits your needs.
    """
    new_kwargs = copy.deepcopy(kwargs)
    for vali in field.validators:
        if isinstance(vali, Email):
            _email_kwargs(new_kwargs)
        if isinstance(vali, EqualTo):
            _equal_to_kwargs(new_kwargs, vali)
        if isinstance(vali, IPAddress):
            _ip_address_kwargs(new_kwargs)
        if isinstance(vali, Length):
            _length_kwargs(new_kwargs, vali)
        if isinstance(vali, NumberRange):
            _number_range_kwargs(new_kwargs, vali)
        if isinstance(vali, Required):
            _required_kwargs(new_kwargs)
            _trigger_kwargs(new_kwargs, u'key')
        if isinstance(vali, Regexp) and not 'data_regexp' in new_kwargs:
            _regexp_kwargs(new_kwargs, vali)
        if isinstance(vali, URL):
            _url_kwargs(new_kwargs)
        if isinstance(vali, AnyOf):
            _anyof_kwargs(new_kwargs, vali)

        if not 'data_trigger' in new_kwargs:
            _trigger_kwargs(new_kwargs)
        if not 'data-error-message' in new_kwargs and vali.message is not None:
            _message_kwargs(new_kwargs, message=vali.message)

    return new_kwargs


def _email_kwargs(kwargs):
    kwargs[u'data-type'] = u'email'


def _equal_to_kwargs(kwargs, vali):
    kwargs[u'data-equalto'] = u'#' + vali.fieldname


def _ip_address_kwargs(kwargs):
    # Regexp from http://stackoverflow.com/a/4460645
    kwargs[u'data-regexp'] =\
        r'^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b$'


def _length_kwargs(kwargs, vali):
    kwargs[u'data-rangelength'] = u'[' + str(vali.min) + u',' + str(vali.max) + u']'


def _number_range_kwargs(kwargs, vali):
    kwargs[u'data-range'] = u'[' + str(vali.min) + u',' + str(vali.max) + u']'


def _required_kwargs(kwargs):
    kwargs[u'data-required'] = u'true'


def _regexp_kwargs(kwargs, vali):
    # Apparently, this is the best way to check for RegexObject Type
    # It's needed because WTForms allows compiled regexps to be passed to the validator
    RegexObject = type(re.compile(''))
    if isinstance(vali.regex, RegexObject):
        regex_string = vali.regex.pattern
    else:
        regex_string = vali.regex
    kwargs[u'data-regexp'] = regex_string


def _url_kwargs(kwargs):
    kwargs[u'data-type'] = u'url'


def _string_seq_delimiter(vali, kwargs):
    # We normally use a comma as the delimiter - looks clean and it's parsley's default.
    # If the strings for which we check contain a comma, we cannot use it as a delimiter.
    default_delimiter = u','
    fallback_delimiter = u';;;'
    delimiter = default_delimiter
    for value in vali.values:
        if value.find(',') != -1:
            delimiter = fallback_delimiter
            break
    if delimiter != default_delimiter:
        kwargs[u'data-inlist-delimiter'] = delimiter
    return delimiter


def _anyof_kwargs(kwargs, vali):
    delimiter = _string_seq_delimiter(vali, kwargs)
    kwargs[u'data-inlist'] = delimiter.join(vali.values)


def _trigger_kwargs(kwargs, trigger=u'change'):
    kwargs[u'data-trigger'] = trigger


def _message_kwargs(kwargs, message):
    kwargs[u'data-error-message'] = message


class ParsleyInputMixin(Input):
    def __call__(self, field, **kwargs):
        kwargs = parsley_kwargs(field, kwargs)
        return super(ParsleyInputMixin, self).__call__(field, **kwargs)


class TextInput(_TextInput, ParsleyInputMixin):
    pass


class PasswordInput(_PasswordInput, ParsleyInputMixin):
    pass


class CheckboxInput(_CheckboxInput, ParsleyInputMixin):
    pass


class Select(_Select):
    def __call__(self, field, **kwargs):
        kwargs = parsley_kwargs(field, kwargs)
        return super(Select, self).__call__(field, **kwargs)


class TextField(_TextField):
    def __init__(self, *args, **kwargs):
        super(TextField, self).__init__(widget=TextInput(), *args, **kwargs)


class IntegerField(_IntegerField):
    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(widget=TextInput(), *args, **kwargs)


class BooleanField(_BooleanField):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(widget=CheckboxInput(), *args, **kwargs)


class DecimalField(_DecimalField):
    def __init__(self, *args, **kwargs):
        super(DecimalField, self).__init__(widget=TextInput(), *args, **kwargs)


class FloatField(_FloatField):
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(widget=TextInput(), *args, **kwargs)


class PasswordField(_PasswordField):
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(widget=PasswordInput(), *args, **kwargs)


class SelectField(_SelectField):
    def __init__(self, *args, **kwargs):
        super(SelectField, self).__init__(widget=Select(), *args, **kwargs)
