# WTForms-ParsleyJS

## What is this?

This is a small library which you can hook into your WTForms form classes in order to enable client side validation.

[WTForms](http://wtforms.simplecodes.com/docs/1.0.4/) allows you to validate your forms on the server side. Ideally, we could reuse these validators on the client side with JavaScript without writing any extra code. This will allow for more direct user feedback in our forms.

This library uses [ParsleyJS](http://parsleyjs.org/documentation.html) for this task. ParsleyJS is a popular client side JavaScript validation library. It is configured using specific HTML markup in the forms.

This library will generate these tags from your WTForms validators.

## Sample

[Check out the sample here](http://vast-plains-1931.herokuapp.com/parsley_testform). You can also run the sample yourself by calling `run_sample.py` if you have flask installed.

## Installation

You can install from pypi using 

`pip install wtforms-parsleyjs`

## What is supported?

The following WTForms validators are supported:

* E-Mail Address
* Matching values
* IP4 Address
* Length of string
* Required field
* Regexp (see limitations)
* URL
* `AnyOf`

The `NoneOf` validator is not supported because this functionality is not supported by ParsleyJS.

The following WTForms widgets are supported:

* TextInput
* Select
* CheckboxInput

Radio Buttons are not supported.

## How to use it?

The easiest way is to simply use the supplied field classes in your form definitions. These subclass the default WTForms field classes and should behave identically to them apart from the extra tags. So instead of importing from wtforms you say for example:

`from wtformsparsleyjs import IntegerField`

If you have your own Field classes, you can use the provided input widgets and pass them into your classes by overwriting the constructor of the underlying default WTForms base field class.

You can also directly use the `ParsleyInputMixin` on your own widget classes or you can directly call the function `parsley_kwargs` which will generate the needed tags for your field (which you can then for example pass in as kwargs to the constructor of the input widget).

## Limitations

Note that the regex validation relies on the regex pattern being compatible with both ECMA script and Python. The regex is not converted in any way.

Notably the ECMA script default behaviour matches the behaviour of [Python's search, not match](http://docs.python.org/2/library/re.html#search-vs-match).

It's possible to simply supply your own `data-regexp` keyword to the field to explicitly provide the ECMA script regex. See [the flask documentation on this](http://flask.pocoo.org/docs/patterns/wtforms/#forms-in-templates). If you do this the library will not touch your custom regex.

Note that the WTForms URL vaidator probably is a bit more liberal than the parsley one. Do check if the behaviour suits your needs.

WTForms-ParsleyJS has been developed and run solely on Python 2.7. - but it may work with other versions.

## Dependencies

Of course ParsleyJS and WTForms are required. ParsleyJS in turn requires jQuery. 

The `AnyOf` validator requires parsleys extra validators which are distributed in a seperate file.

The sample uses the [Flask web framework](http://flask.pocoo.org/docs/) and [Twitter Bootstrap](http://twitter.github.io/bootstrap/). Because the sample should run out of the box on Heroku, ParsleyJS is included as a git submodule.


## What else?

If you have any improvements or feedback please let me know or send me a pull request.

The license is MIT.