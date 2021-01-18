
--正确的，成立时允许下推
(
(exists (select 1 from t_sal_orderPlan c where c.FControlSend='SEND' and c.FISOUTSTOCKBYRECAMOUNT='1' and c.FId=FID) OR   
not exists (select 1 from t_sal_orderPlan a inner join
                  (select sum(FRECADVANCEAMOUNT) as FRecAdvanceAmount,sum(FRecAmount) as FRecAmount,FID
                  from t_sal_OrderPlan 
                  where FControlSend='SEND' 
                  group by FID) b on a.FID=b.FID where b.Frecadvanceamount<>b.FRecAmount and a.FId=FID )
OR exists (select 1 from T_SAL_ORDER od where od.F_HDIN_SpecialApproval=1 and od.FID=FID)
)
AND
(not exists(select 1  from t_sal_order t1 join hd_khhmd t2 on t1.FCUSTID=t2.FKHID WHERE T1.FID=FID) )
)