import django_tables2 as tables
from silo.models import ValueStore

TEMPLATE = '''
   <a class="btn btn-default btn-xs" role="button" href="/value_edit/{{ record.id }}">Edit</a>
   <a class="btn btn-danger btn-xs" role="button" href="/value_delete/{{ record.id }}">Delete</button>
'''

TEMPLATE2 = '''
<a data-toggle="modal" href="/field_edit/{{ record.field.id }}" data-target="#columnModal">{{record.field}}</a>
'''

class SiloTable(tables.Table):
	edit = tables.TemplateColumn(TEMPLATE)
	field = tables.TemplateColumn(TEMPLATE2)
	class Meta:
		model = ValueStore
		attrs = {"class": "paleblue"}