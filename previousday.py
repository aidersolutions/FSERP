#unused files
%run psetup.py
import settings
settings.level=10
from report_tryton import Hygiene
hygiene=Hygiene()
data={}
data['code']=111
data['organization']='settings'
import datetime
datetime.datetime.strptime('18/08/2015','%d/%m/%Y')
date_set=datetime.datetime.strptime('18/08/2015','%d/%m/%Y')
data['organization']='settings'
data['organization']='settings'
data['date']=date_set
data['test']='new_settings'
data['description']='passing a test image'
data['report']=open('/home/jitesh/qt/settings.png').read()
hygiene.cpest_report(data)
Pest=Model.get('health_and_hygiene.pest_control_test')
pest=Pest()
pest.organization='Settings'
pest.code=1
pest.date=date_set
date.test='settings'
pest.test='settings'
pest.description='settings'
pest.report=data['report']
pest.save()
data['report']
%history
%history?
%history -f previousday.py
