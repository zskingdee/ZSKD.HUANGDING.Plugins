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
    [Description("定时任务：送货计划欠数大于0更新天数")]
    public class SHJH_UpdateDay : IScheduleService
    {
        public void Run(Context ctx, Schedule schedule)
        {
            string sql =
              "/*dialect*/update t_Pur_DeliveryPlanEntry set FEXPIRYDAYS = isnull(DATEDIFF(day, getdate(), t1.F_CGDDJHDATE), 0)  from t_Pur_DeliveryPlanEntry t1 where t1.FOweQty > 0";
            DBUtils.Execute(ctx, sql);
        }
    }
}
