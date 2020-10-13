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
			FRECEIPTCONDITIONID=dataobj["FRECEIPTCONDITIONID"]
			if FRECEIPTCONDITIONID<>None:
			#{
				ReceiptConditionControl=dataobj["FRECEIPTCONDITIONID"]["F_HDIN_SpecialApproval"] #收款条件是否勾选预收特批控制
				if ReceiptConditionControl==True:
				#{
					sql="/*dialect*/select distinct t2.FBILLNO from T_SAL_DELIVERYNOTICEENTRY t1 join T_SAL_ORDER t2 on t1.FORDERNO=t2.FBILLNO "
					sql=sql+" join T_SAL_ORDERPLAN t3 on t2.FID=t3.FID and t3.FNEEDRECADVANCE=1 and t3.FRECADVANCEAMOUNT>t3.FRECAMOUNT "
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
						e.CancelMessage="销售订单"+SEOrders+"的收款计划是预收类型，但实收金额小于应收金额，提交失败。"
					#}
				#}
			#}
		#}
	#}
def OnPreparePropertys(e):
	e.FieldKeys.Add("FRECEIPTCONDITIONID");