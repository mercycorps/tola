import django_tables2 as tables

TEMPLATE = '''
   <a class="btn btn-default btn-xs" role="button" href="/value_edit/{{ record.id }}">Edit</a>
   <a class="btn btn-danger btn-xs" role="button" href="/value_delete/{{ record.id }}">Delete</button>
'''

TEMPLATE2 = '''
<a data-toggle="modal" href="/field_edit/{{ record.field.id }}" data-target="#columnModal">{{record.field}}</a>
'''
"""
class SiloTable(tables.Table):
    edit = tables.TemplateColumn(TEMPLATE)
    field = tables.TemplateColumn(TEMPLATE2)
    class Meta:
        model = ValueStore
        attrs = {"class": "paleblue"}
"""


def define_table(columns):
    from django.template.base import add_to_builtins
    add_to_builtins('silo.templatetags.underscoretags')
    
    """
    Dynamically builds a django-tables2 table without specifying the column names
    It is important to build the django-tables2 dynamically because each time a silo 
    is loaded from MongoDB, it is not known what columns heading it has or how mnay columns it has
    """
    EDIT_DEL_TEMPLATE = '''
        <a class="btn btn-default btn-xs" role="button" href="/value_edit/{{ record|get:'_id'|get:'$oid' }}">Edit</a>
        <a class="btn btn-danger btn-xs btn-del" style="color: #FFF;" role="button" href="/value_delete/{{ record|get:'_id'|get:'$oid'  }}" title="Are you sure you want to delete this record?">Delete</a> 
        '''
    #add the operations to the table first then append the dynamic table columns
    attrs = {}
    attrs['Operation'] = tables.TemplateColumn(EDIT_DEL_TEMPLATE)
    attrs.update(dict((c, tables.Column()) for c in columns))
    attrs['Meta'] = type('Meta', (), dict(exclude=["_id", "edit_date", "create_date"], attrs={"class":"paleblue", "orderable":"True", "width":"100%"}) )
    
    klass = type('DynamicTable', (tables.Table,), attrs)
    return klass
