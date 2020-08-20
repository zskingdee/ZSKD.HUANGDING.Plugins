using Kingdee.BOS;
using Kingdee.BOS.App.Data;
using Kingdee.BOS.Core.DynamicForm.PlugIn;
using Kingdee.BOS.Core.DynamicForm.PlugIn.Args;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ZSKD.HUANGDING.Plugins
{
    [System.ComponentModel.Description("收料通知反写送货计划")]
    public class ReverseReceiptNotice: AbstractOperationServicePlugIn
    {


        [HotUpdate]
        [Description("更新送货计划的收料数量,到期天数,发送供应商日期")]
        public override void EndOperationTransaction(EndOperationTransactionArgs e)
        {

            // DynamicObject dy = e.DataEntitys[0] as DynamicObject;
            foreach (DynamicObject dy in e.DataEntitys)
            {
                int InboundId = Convert.ToInt32(dy["Id"]);
                DynamicObjectCollection PUR_ReceiveEntry = dy["PUR_ReceiveEntry"] as DynamicObjectCollection;

                //   Dictionary<int, float> keyValuePairs = new Dictionary<int, float>();
                for (int i = 0; i < PUR_ReceiveEntry.Count; i++)
                {
                    DynamicObject EntryValue = PUR_ReceiveEntry[i];
                    int entryId = Convert.ToInt32(EntryValue["Id"]);
                    string sql =
                    "/*dialect*/update t_Pur_DeliveryPlanEntry set  FRECEIPTQTY=t5.FMUSTQTY,FEXPIRYDAYS=isnull(DATEDIFF(day,getdate(),t1.F_CGDDJHDATE))  from t_Pur_DeliveryPlanEntry t1               " +
                    " join t_Pur_DeliveryPlanEntry_LK t2 on t1.FEntryID = t2.FEntryID and t2.FSTableName = 't_PUR_POOrderEntry'    " +
                    " join t_PUR_POOrderEntry t3 on t3.FID = t2.FSBillId    and t3.FEntryID=t2.FSID                                                         " +
                    " join T_PUR_RECEIVEENTRY_LK t4 on t4.FSBILLID = t3.FID and t3.FEntryID=t4.FSID and t4.FSTABLENAME = 't_PUR_POOrderEntry'              " +
                    " join T_PUR_RECEIVEENTRY t5 on t5.FENTRYID = t4.FENTRYID    join T_PUR_Receive t6 on t6.FID=t5.FID " +
                    " where t5.FENTRYID = " + entryId;
                    DBUtils.Execute(Context, sql);
                }


            }
        }
  


    }
}
