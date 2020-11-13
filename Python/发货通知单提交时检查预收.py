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
def BeforeExecuteOperationTransaction(e):
    #发货通知单提交时检查预收
    if this.FormOperation.Operation=="Submit":
    #{
        for dataobj in e.SelectedRows:
        #{
            sql="/*dialect*/select distinct t2.FBILLNO from T_SAL_DELIVERYNOTICEENTRY t1 join T_SAL_ORDER t2 on t1.FORDERNO=t2.FBILLNO "
            sql=sql+" join (select sum(FRECADVANCEAMOUNT) as FRecAdvanceAmount,sum(FRecAmount) as FRecAmount,FID from t_sal_OrderPlan "
            sql=sql+" where FControlSend='SEND' group by FID) t3 on t2.FID=t3.FID and t3.FRECADVANCEAMOUNT<>t3.FRECAMOUNT " #实收不等于应收时
            sql=sql+" and t3.FID not in(select FID from t_sal_orderPlan c where c.FControlSend='SEND' and c.FISOUTSTOCKBYRECAMOUNT='1') " #按实际预收控制发货 未勾选
            sql=sql+" join T_SAL_DELIVERYNOTICE t4 on t4.FID=t1.FID and t4.F_HDIN_SpecialApproval<>1 "
            sql=sql+" where t1.FID="+str(dataobj["ID"])
            #raise Exception("提示信息！"+str(dataobj["FRECEIPTCONDITIONID"]["Number"]))
            rows=DBUtils.ExecuteDynamicObject(this.Context,sql);
            SEOrders=""
            if rows.Count>0:
                for row in rows:
                    SEOrders=SEOrders+row["FBILLNO"]+","
            if SEOrders!="":
            #{
                e.Cancel=True
                e.CancelMessage="销售订单"+SEOrders+" 通过预收控制发货，需要预收的实收金额之和等于应收金额之和，提交失败。"
            #}
		#}
	#}
def OnPreparePropertys(e):
    e.FieldKeys.Add("FRECEIPTCONDITIONID");