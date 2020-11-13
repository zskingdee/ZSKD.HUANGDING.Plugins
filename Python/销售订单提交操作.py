import clr
clr.AddReference("Kingdee.BOS")
clr.AddReference("Kingdee.BOS.App")
clr.AddReference("Kingdee.BOS.Core")
clr.AddReference("Kingdee.BOS.DataEntity")
clr.AddReference("Kingdee.BOS.ServiceHelper")
clr.AddReference("Kingdee.K3.SCM.App.Sal.ServicePlugIn")
from Kingdee.BOS import *
from Kingdee.BOS.Util import *
from Kingdee.BOS.Core.Bill import *
from Kingdee.BOS.Core.DynamicForm import *
from Kingdee.BOS.Core.DynamicForm.PlugIn import *
from Kingdee.BOS.Core.DynamicForm.PlugIn.ControlModel import *
from Kingdee.BOS.App.Data import *
from Kingdee.BOS.Core.Permission import *
from Kingdee.BOS.ServiceHelper import *
from Kingdee.K3.SCM.App.Sal.ServicePlugIn.SaleOrder import *
import Kingdee.K3.SCM.App.Sal.ServicePlugIn.SaleOrder as ServSalOrder
from System import *

def OnAddValidators(e):
    for dataobj in e.DataEntities:
        FID=dataobj["ID"]
        F_HDIN_SpecialApproval=dataobj["F_HDIN_SpecialApproval"]
        sql="/*dialect*/select distinct F_Hdin_CheckBox from T_SAL_ORDER where FID= "+str(FID)
        rows=DBUtils.ExecuteDynamicObject(this.Context,sql);

        if rows.Count>0:
            F_HDIN_SpecialApproval=int(rows[0]["F_HDIN_SpecialApproval"])

        if F_HDIN_SpecialApproval==0:
            item=ServSalOrder.SubmitValidator()
            item.AlwaysValidate = True
            item.EntityKey = "FBillHead"
            e.Validators.Add(item);
            break;
        #F_HDIN_SpecialApproval  F_HDIN_CHECKBOX

def OnPreparePropertys(e):
    e.FieldKeys.Add("FPrice");
    e.FieldKeys.Add("FTaxPrice");
    e.FieldKeys.Add("FPriceUnitId");
    e.FieldKeys.Add("FTaxNetPrice");
    e.FieldKeys.Add("FLimitDownPrice");
    e.FieldKeys.Add("FIsIncludedTax");
    e.FieldKeys.Add("FMaterialId");
    e.FieldKeys.Add("FUnitId");
    e.FieldKeys.Add("FSettleCurrId");
    e.FieldKeys.Add("FIsFree");
    e.FieldKeys.Add("FPriceCoefficient");
    e.FieldKeys.Add("FSysPrice");
    e.FieldKeys.Add("F_Hdin_CheckBox");

