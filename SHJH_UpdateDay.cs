using Kingdee.BOS;
using Kingdee.BOS.App.Data;
using Kingdee.BOS.Contracts;
using Kingdee.BOS.Core;
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
    [Description("定时任务：销售出库单汇总生成直接调拨单")]
    public class SHJH_UpdateDay : IScheduleService
    {
        public void Run(Context ctx, Schedule schedule)
        {
            string sql =
              "/*dialect*/update t_Pur_DeliveryPlanEntry set  FEXPIRYDAYS=isnull(DATEDIFF(day,getdate(),t1.F_CGDDJHDATE),0)  from t_Pur_DeliveryPlanEntry t1               " +
                    " join t_Pur_DeliveryPlanEntry_LK t2 on t1.FEntryID = t2.FEntryID and t2.FSTableName = 't_PUR_POOrderEntry'    " +
                    " join t_PUR_POOrderEntry t3 on t3.FID = t2.FSBillId    and t3.FEntryID=t2.FSID                                                         " +
                    " join T_PUR_RECEIVEENTRY_LK t4 on t4.FSBILLID = t3.FID and t3.FEntryID=t4.FSID and t4.FSTABLENAME = 't_PUR_POOrderEntry'              " +
                    " join T_PUR_RECEIVEENTRY t5 on t5.FENTRYID = t4.FENTRYID    join T_PUR_Receive t6 on t6.FID=t5.FID " +
                      "  where t1.FEXPIRYDAYS>0";
            DBUtils.Execute(ctx, sql);
        }
    }
}
