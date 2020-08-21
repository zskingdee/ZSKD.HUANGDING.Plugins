import clr
clr.AddReference("Kingdee.BOS")
clr.AddReference("Kingdee.BOS.App")
clr.AddReference("Kingdee.BOS.Core")
clr.AddReference("Kingdee.BOS.DataEntity")
clr.AddReference("Kingdee.BOS.ServiceHelper")
from Kingdee.BOS.Core.List.PlugIn import *
from Kingdee.BOS.Core.List import *
from Kingdee.BOS.Core.DynamicForm import *
from Kingdee.BOS.App.Data import *
from Kingdee.BOS.Core.Permission import *
from Kingdee.BOS.ServiceHelper import *
from System import *
def AfterBindData(e):
	#默认显示合同变更查询按钮
	this.View.GetMainBarItem('tbChangeLog').Visible=True;