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
	#发货通知单预收特批操作
	if this.FormOperation.Operation=="SpecialApproval":
		for dataobj in e.DataEntitys:
            #F_HDIN_SpecialApproval  F_HDIN_CHECKBOX
			sql="update T_SAL_DELIVERYNOTICE set F_HDIN_SpecialApproval=1 where FID="+str(dataobj["ID"])
			#raise Exception("提示信息！"+str(dataobj["ID"]))
			DBUtils.Execute(this.Context,sql);
	elif this.FormOperation.Operation=="UnSpecialApproval":
		for dataobj in e.DataEntitys:
			sql="update T_SAL_DELIVERYNOTICE set F_HDIN_SpecialApproval=0 where FID="+str(dataobj["ID"])
			#raise Exception("提示信息！"+str(dataobj["ID"]))
			DBUtils.Execute(this.Context,sql);