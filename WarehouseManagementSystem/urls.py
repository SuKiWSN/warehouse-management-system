from django.conf.urls import url
from . import profile_page, vertify, home_page, usercost
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles


urlpatterns = [
    url('profile/', profile_page.test),
    url('regist/', profile_page.regist),
    url('vertify/', vertify.mail_code),
    url('login_check/', profile_page.login_check),
    url('manage/', home_page.manage),
    url('user/', home_page.get_user),
    url('modify/', home_page.modify),
    url('changepwd/', home_page.changepwd),
    url('getrole/', home_page.getrole),
    url('getusers/', home_page.getusers),
    url('showpicture/', home_page.getpicture),
    url('search_usr/', home_page.search_usr),
    url('addusr/', home_page.add_user),
    url('deleteusr/', home_page.deleteusr),
    url('inmoney/', home_page.inmoney),
    url('getrechargerecord/', home_page.get_Rechargerecord),
    url('user_spend', usercost.user_spend),
    url('consumerecord/', usercost.consume_record),
    url('changepower/', home_page.changerole),
    url('changegender/', home_page.changegender),
    url('changeage/', home_page.changeage),
    url('change/', home_page.change),
    url('deletebill/', home_page.deletebill),
    url('addbill/', home_page.addbill),
    url('mdfbill/', home_page.mdfbill),
    url('mdfrole/', home_page.mdfrole),
    url('deleterole/', home_page.deleterole),
    url('addrole/', home_page.addrole),
    url('getdepartment/', home_page.getdepartment),
    url('mdfdept/', home_page.mdfdept),
    url('deletedept/', home_page.deletedept),
    url('adddept/', home_page.adddept),
    url('changedept/', home_page.changedept),
    url('getalarm/', home_page.getalarm),
    url('processalarm/', home_page.processalarm),
    url('getdetail/', home_page.getdetail),
    url('deletealarm/', home_page.deletealarm),
    url('multiop/', home_page.multiop),
    url('', profile_page.redirect),
]