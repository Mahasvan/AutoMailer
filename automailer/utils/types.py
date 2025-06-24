from typing import TypeVar
from automailer.core.template import TemplateModel

# make a type for all TemplateModel subclasses
TemplateModelType = TypeVar('TemplateModelType', bound='TemplateModel')
