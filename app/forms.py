from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class TextForm(Form):
    text = TextAreaField('textid', default="Loja is city of Ecauador")
    #remember_me = BooleanField('remember_me', default = False)