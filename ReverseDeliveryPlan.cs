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
    [HotUpdate]
    [System.ComponentModel.Description("采购入库反写送货计划，更新送货计划的入库数量,欠数")]
   public class ReverseDeliveryPlan : AbstractOperationServicePlugIn
    {



     
        public override void EndOperationTransaction(EndOperationTransactionArgs e)
        {

         //   DynamicObject dy = e.DataEntitys[0] as DynamicObject;

            foreach (DynamicObject dy in e.DataEntitys ){
                int InboundId = Convert.ToInt32(dy["Id"]);
                DynamicObjectCollection InStockEntry = dy["InStockEntry"] as DynamicObjectCollection;

                //   Dictionary<int, float> keyValuePairs = new Dictionary<int, float>();

                for (int i = 0; i < InStockEntry.Count; i++) {
                    DynamicObject EntryValue = InStockEntry[i];
                    int entryId = Convert.ToInt32(EntryValue["Id"]);
                    string sql =
    "/*dialect*/update t_Pur_DeliveryPlanEntry set  FInStockQty = t7.FREALQTY,FOweQty=(t1.FQTY-t7.FREALQTY)  from t_Pur_DeliveryPlanEntry t1               " +
    "join t_Pur_DeliveryPlanEntry_LK t2 on t1.FEntryID = t2.FEntryID and t2.FSTableName = 't_PUR_POOrderEntry'    " +
    "join t_PUR_POOrderEntry t3 on t3.FID = t2.FSBillId   and t3.FEntryID=t2.FSID                   " +
    "join T_PUR_RECEIVEENTRY_LK t4 on t4.FSBILLID = t3.FID and t3.FEntryID=t4.FSID and t4.FSTABLENAME = 't_PUR_POOrderEntry'              " +
    "join T_PUR_RECEIVEENTRY t5 on t5.FENTRYID = t4.FENTRYID                                                      " +
    "join T_STK_INSTOCKENTRY_LK t6 on t6.FSBILLID = t5.FID and t5.FEntryID=t6.FSID  and t6.FSTABLENAME = 'T_PUR_ReceiveEntry'              " +
    "join T_STK_INSTOCKENTRY t7 on t7.FENTRYID = t6.FENTRYID   " +
    "  where t7.FENTRYID = " + entryId;
                    DBUtils.Execute(Context, sql);

                }


            } }

    }
}
