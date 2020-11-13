import clr
clr.AddReference("Kingdee.BOS")
clr.AddReference("Kingdee.BOS.App")
clr.AddReference("Kingdee.BOS.Core")
clr.AddReference("Kingdee.BOS.DataEntity")
clr.AddReference("Kingdee.BOS.ServiceHelper")
from Kingdee.BOS import *
from Kingdee.BOS.Util import *
from Kingdee.BOS.Core.Bill import *
from Kingdee.BOS.Core.DynamicForm import *
from Kingdee.BOS.Core.DynamicForm.PlugIn import *
from Kingdee.BOS.Core.DynamicForm.PlugIn.ControlModel import *
from Kingdee.BOS.App.Data import *
from Kingdee.BOS.Core.Permission import *
from Kingdee.BOS.ServiceHelper import *
from System import *
def EndOperationTransaction(e):
	#采购退料单审核操作反写送货计划关闭状态
    for dataobj in e.DataEntitys:
        #行业务关闭状态
        sql="/*dialect*/update t1 set t1.FMRPCLOSESTATUS=t3.FMRPCLOSESTATUS from t_Pur_DeliveryPlanEntry t1 "
        sql=sql+" join t_Pur_DeliveryPlanEntry_LK t2 on t1.FEntryID=t2.FEntryID "
        sql=sql+" join t_PUR_POOrderEntry t3 on t2.FSID=t3.FEntryID "
        sql=sql+" join t_PUR_POOrder t4 on t3.FID=t4.FID "
        sql=sql+" join T_PUR_MRBENTRY t5 on t5.FORDERNO=t4.FBillNo where t5.FID="+str(dataobj["ID"])
        #整单关闭
        sql=sql+"\n update t_Pur_DeliveryPlan set FCLOSESTATUS='B' where FID not in (select t1.FID from t_Pur_DeliveryPlanEntry t1 "
        sql=sql+" where FMRPCLOSESTATUS='A') "
        #整单反关闭
        sql=sql+"\n update t_Pur_DeliveryPlan set FCLOSESTATUS='A' where FID in (select t1.FID from t_Pur_DeliveryPlanEntry t1 "
        sql=sql+" where FMRPCLOSESTATUS='A') "
        #raise NameError(sql)
        DBUtils.Execute(this.Context,sql);