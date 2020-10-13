import clr
clr.AddReference("Kingdee.BOS")
clr.AddReference("Kingdee.BOS.App")
clr.AddReference("Kingdee.BOS.Core")
clr.AddReference("Kingdee.BOS.DataEntity")
clr.AddReference("Kingdee.BOS.ServiceHelper")
clr.AddReference("Kingdee.BOS.OrmEngine")
from Kingdee.BOS import *
from Kingdee.BOS.Util import *
from Kingdee.BOS.Core import *
from Kingdee.BOS.Core.Bill import *
from Kingdee.BOS.Core.DynamicForm import *
from Kingdee.BOS.Core.DynamicForm.PlugIn import *
from Kingdee.BOS.Core.DynamicForm.PlugIn.ControlModel import *
from Kingdee.BOS.App.Data import *
from Kingdee.BOS.Core.Permission import *
from Kingdee.BOS.ServiceHelper import *
from Kingdee.BOS.Orm.Drivers import *
from Kingdee.BOS.Orm import *
from Kingdee.BOS.Core.Msg import *
import Kingdee.BOS.Orm.DataEntity as de
from System import *
def BarItemClick(e):
    #销售订单申请特批
    if e.BarItemKey=="Hdin_ReqSpecial":
        MessageId=str(SequentialGuid.NewGuid());
        Title="销售订单预收特批申请";
        Content = "我正在申请销售订单预收特批，请您点击消息上方【查看单据】。";
        SenderId = str(this.Context.UserId);
        ObjectTypeId = "SAL_SaleOrder";
        KeyValue = str(this.View.Model.DataObject["Id"]);
        RECEIVERSDISP=""
        
        sql="select t2.FUSERID,t3.FName from t_SEC_role t1 join T_SEC_ROLEUSER t2 on t1.FROLEID=t2.FROLEID and t1.FNUMBER='SpecialApproval' join T_SEC_user t3 on t2.FUSERID=t3.FUSERID"
        userRows=DBServiceHelper.ExecuteDynamicObject(this.Context,sql);
        if userRows.Count>0:
            for userRow in userRows:
                RECEIVERSDISP=RECEIVERSDISP+userRow["FName"]+","
            RECEIVERSDISP=RECEIVERSDISP[:-1] #删除最后多余的逗号
            
            #信息头
            sql="insert into T_WF_MESSAGESEND(FMESSAGEID,FTITLE,FCONTENT,FSENDERID,FCREATETIME,FRECEIVERID,FCOMPLETEDTIME,FSTATUS,FTYPE,"
            sql=sql+"FOBJECTTYPEID,FKEYVALUE,FSENDMSGID,FRECEIVERSDISP,FATTACHDATA,FFILEUPDATE)values("
            sql=sql+"'"+MessageId+"','"+Title+"','"+Content+"',"+SenderId+",GETDATE(),null,null,0,1,"
            sql=sql+"'"+ObjectTypeId+"',"+KeyValue+",'','demo','',null)"

            #信息体
            for userRow in userRows:
                sql=sql+" \n "
                sql=sql+"insert into T_WF_MESSAGE(FMESSAGEID,FTITLE,FCONTENT,FSENDERID,FCREATETIME,FRECEIVERID,FCOMPLETEDTIME,FSTATUS,FTYPE,"
                sql=sql+"FOBJECTTYPEID,FKEYVALUE,FSENDMSGID,FRECEIVERSDISP,FATTACHDATA,FFILEUPDATE,FPROCINSTID,FACTIVITYID)values("
                sql=sql+"'"+str(SequentialGuid.NewGuid())+"','"+Title+"','"+Content+"',"+SenderId+",GETDATE(),"+str(userRow["FUSERID"])+",NULL,0,1,"
                sql=sql+"'"+ObjectTypeId+"',"+KeyValue+",'"+MessageId+"','"+RECEIVERSDISP+"','',NULL,'',0)"

            DBServiceHelper.Execute(this.Context,sql);
            this.View.ShowMessage("发送成功，已通知："+RECEIVERSDISP);
        else:
            this.View.ShowMessage("没有可以接收消息的人，请联系管理员为【预收特批组】角色添加人员！");