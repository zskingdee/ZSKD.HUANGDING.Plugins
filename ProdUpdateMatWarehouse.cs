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
{[Kingdee.BOS.Util.HotUpdate]
    [System.ComponentModel.Description("生产订单保存时更新生产生产用料的对应的仓库")]
    public class ProdUpdateMatWarehouse:AbstractOperationServicePlugIn
    {
        public override void EndOperationTransaction(EndOperationTransactionArgs e)
        {
             DynamicObject dy = e.DataEntitys[0] as DynamicObject;
            string BillNo = Convert.ToString(dy["BillNo"]);
            string sql =
                   "/*dialect*/update T_PRD_PPBOMENTRY_C set FSTOCKID=t4.FWIPSTOCKID from T_PRD_PPBOMENTRY t1    "  +
                   " join T_PRD_PPBOMENTRY_C t1_c on t1.FENTRYID = t1_c.FENTRYID   and (t1_c.FISSUETYPE=2 or t1_c.FISSUETYPE=4)                              " +
                   " join T_PRD_PPBOM t2 on t1.FID = t2.FID                                                      "  +
                   " join T_PRD_MOENTRY t3 on t2.FMOID = t3.FID and t3.FENTRYID = t2.FMOENTRYID                  "  +
                   " join T_BD_DEPARTMENT t4 on t3.FWORKSHOPID = t4.FDEPTID and t4.FWIPSTOCKID > 0               "  +
                   " where t1.FMOBILLNO = '" + BillNo+"'";
            DBUtils.Execute(Context, sql);
           


        }
    }
}
