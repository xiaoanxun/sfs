# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 21:24:35 2023

@author: yan
"""
import pandas as pd
import numpy as np
import datetime
from pyecharts.charts import *
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Funnel
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


#导入数据
df = pd.read_csv("D:/YNUFE/研一下/数据科学与工程/yanyan/data.csv",index_col=None)
df.info()

df.head()

df.describe()

df.drop_duplicates(inplace=True)
df.head()

df.isnull().sum()

df['time']=pd.to_datetime(df['time'])
df.info()

df['date'] = df.time.dt.date
df['hour'] = df.time.dt.hour
df.head()

df['user_id'] = df.user_id.values.astype('str')
df['item_id'] = df.item_id.values.astype('str')
df['behavior_type'] = df.behavior_type.values.astype('str')
df.info()

df['item_category'] = df.item_category.values.astype('str')

#提取数据
pv_day = df[df.behavior_type =='1'].groupby('date')['behavior_type'].count()
uv_day = df[df.behavior_type =='1'].drop_duplicates(['user_id','date']).groupby('date')['user_id'].count()
#转换成图表所需的格式（list）
#1、日期（list.index）
date = pv_day.index
#2、pv、uv（list.values）
pv = np.around(pv_day.values/10000,decimals=2)
uv = np.around(uv_day.values/10000,decimals=2)

# 制作图表
x=list(date)
y1=pv
y2=uv
pvuv_day_line = (Line(init_opts=opts.InitOpts(theme=ThemeType.DARK)) #主题设置
       .add_xaxis(x) #x轴数据源
       .add_yaxis('pv',#图例名字
                  y1, #y1轴数据源
                  label_opts=opts.LabelOpts(is_show=False) #不显示数据标签
                 )
       .add_yaxis('uv',#图例名字
                  yaxis_index=1, #Y的双轴1号索引（区别于y1轴）
                  y_axis=y2, #y2轴数据源
                  label_opts=opts.LabelOpts(is_show=False) #不显示数据标签
                 ) 
        .extend_axis( #y2的轴设置 
                    yaxis=opts.AxisOpts(
                                        name='uv',#轴名字
                                        min_=0,#轴起点值
                                        max_=1.6, #轴最大值
                                        interval=0.4, #轴区间间隔
                                        axislabel_opts=opts.LabelOpts(formatter="{value} 万人") #轴数据标签格式设置
                                         )
                    )
        .set_global_opts( #全局设置
                        tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis",axis_pointer_type='cross'), #随鼠标位置显示xy轴的数据、聚焦形式(交叉)
                        xaxis_opts=opts.AxisOpts(type_='category',axispointer_opts=opts.AxisPointerOpts(is_show=True,type_="shadow")),#随鼠标位置凸显x轴长条、凸显形式（阴影）
                        yaxis_opts=opts.AxisOpts(name='pv',axislabel_opts=opts.LabelOpts(formatter="{value} 万次")),#y1轴(默认轴)名字、轴数据标签格式设置
                        title_opts=opts.TitleOpts(title="每日pv和uv") #标题        
                         )              
            )
#pvuv_day_line.render_notebook() #展示图表
make_snapshot(snapshot, pvuv_day_line.render(), "pvuv_day_line.png")

#制作每日用户行为总量的数据表
view_day = df[df.behavior_type =='1'].groupby('date')['behavior_type'].count()
col_day = df[df.behavior_type =='2'].groupby('date')['behavior_type'].count()
add_day = df[df.behavior_type =='3'].groupby('date')['behavior_type'].count()
buy_day = df[df.behavior_type =='4'].groupby('date')['behavior_type'].count()
behavier_day = pd.merge(view_day, col_day, how='outer', on='date', suffixes=('_view', '_col')).merge(add_day, how='outer', on='date', suffixes=('_col', '_add')).merge(buy_day, how='outer', on='date', suffixes=('_add', '_buy'))
behavier_day.columns=['view','col','add','buy']
behavier_day.head()

df['date'] = pd.to_datetime(df['date'])
#提取数据
#日常各时段行为总量
daily_df = df[~df['date'].isin(['2014-12-11','2014-12-12'])]
view_hour = daily_df[daily_df.behavior_type =='1'].groupby('hour')['behavior_type'].count()
col_hour = daily_df[daily_df.behavior_type =='2'].groupby('hour')['behavior_type'].count()
add_hour = daily_df[daily_df.behavior_type =='3'].groupby('hour')['behavior_type'].count()
buy_hour = daily_df[daily_df.behavior_type =='4'].groupby('hour')['behavior_type'].count()
#双12各时段行为总量 （日期说明：因双十二开启时间为12月12号零点，活动期间用户行为主要发生时间在11号到12号，因此本次活动分析时筛选的时间为这两天）
active_df = df[df['date'].isin(['2014-12-11','2014-12-12'])]
view_active_ahour = active_df[active_df.behavior_type =='1'].groupby('hour')['behavior_type'].count()
col_active_ahour = active_df[active_df.behavior_type =='2'].groupby('hour')['behavior_type'].count()
add_active_ahour = active_df[active_df.behavior_type =='3'].groupby('hour')['behavior_type'].count()
buy_active_ahour = active_df[active_df.behavior_type =='4'].groupby('hour')['behavior_type'].count()

# 制作图表
x=col_hour.index.tolist()
#双12
y5=np.around(col_active_ahour.values/2,decimals=0).tolist()
y6=np.around(add_active_ahour.values/2,decimals=0).tolist()
y7=np.around(buy_active_ahour.values/2,decimals=0).tolist()


active_line = (Line()
       .add_xaxis(x) 
       .add_yaxis('收藏',
                  y_axis=y5, 
                  label_opts=opts.LabelOpts(is_show=False) 
                 ) 
       .add_yaxis('加购',
                  y_axis=y6, 
                  label_opts=opts.LabelOpts(is_show=False)
                 ) 
       .add_yaxis('购买',
                  y_axis=y7, 
                  label_opts=opts.LabelOpts(is_show=False) 
                 ) 
        .set_global_opts( 
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis",axis_pointer_type='cross'), 
            legend_opts=opts.LegendOpts(pos_top='5%'),
            xaxis_opts=opts.AxisOpts(type_='category',axispointer_opts=opts.AxisPointerOpts(is_show=True,type_="shadow")),
            yaxis_opts=opts.AxisOpts(name='人次',
                                     axislabel_opts=opts.LabelOpts(formatter="{value}")),
            title_opts=opts.TitleOpts(title="双12日均各时段用户行为",pos_top='0%')        
                        )              
            )

#active_line.render_notebook()
make_snapshot(snapshot, active_line.render(), "active_line.png")
# 制作图表
x=col_hour.index.tolist()
y1=np.around(view_hour.values/29,decimals=0).tolist()
y8=np.around(view_active_ahour.values/2,decimals=0).tolist()

bar=(
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(xaxis_data=x)
    .add_yaxis(
    "日常PV",
        y1,
        stack='stack1',
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
    "双12PV",
        y8,
        stack='stack1',
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="日常和双12每日时段PV走势对比"),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        yaxis_opts=opts.AxisOpts(name='人次',
                                axislabel_opts=opts.LabelOpts(formatter="{value}"))
    )
)

#bar.render_notebook()
make_snapshot(snapshot, bar.render(), "bar.png")

#准备数据
#日常各时段购买率
daily_df = df[~df['date'].isin(['2014-12-11','2014-12-12'])]
view_user_num = daily_df[daily_df.behavior_type =='1'].drop_duplicates(['user_id','date','hour']).groupby('hour')['behavior_type'].count()
buy_user_num = daily_df[daily_df.behavior_type =='4'].drop_duplicates(['user_id','date','hour']).groupby('hour')['behavior_type'].count()
daily_buy_rate = buy_user_num/view_user_num
#双12各时段购买率
active_df = df[df['date'].isin(['2014-12-11','2014-12-12'])]
view_active_user_num = active_df[active_df.behavior_type =='1'].drop_duplicates(['user_id','date','hour']).groupby('hour')['behavior_type'].count()
buy_active_user_num = active_df[active_df.behavior_type =='4'].drop_duplicates(['user_id','date','hour']).groupby('hour')['behavior_type'].count()
acitve_buy_rate = buy_active_user_num/view_active_user_num

x=view_hour.index.tolist() 
y1 = np.around(daily_buy_rate,decimals=2).tolist()
y2 = np.around(acitve_buy_rate,decimals=2).tolist()

buy_rate_line = (Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
       .add_xaxis(x) 
       .add_yaxis('日常购买率',
                  y_axis=y1, 
                  label_opts=opts.LabelOpts(is_show=True) 
                 )
       .add_yaxis('双12购买率',
                  y_axis=y2, 
                  label_opts=opts.LabelOpts(is_show=True) 
                 ) 
        .set_global_opts( 
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis",axis_pointer_type='cross'),
            xaxis_opts=opts.AxisOpts(type_='category',axispointer_opts=opts.AxisPointerOpts(is_show=True,type_="shadow")),
            yaxis_opts=opts.AxisOpts(name=' ',axislabel_opts=opts.LabelOpts(formatter="{value}")),
            title_opts=opts.TitleOpts(title="不同时段购买率"), 
            legend_opts=opts.LegendOpts(pos_top='5%') 
                        )              
            )
#buy_rate_line.render_notebook()
make_snapshot(snapshot, buy_rate_line.render(), "buy_rate_line.png")
#提取数据
#日常各时段行为数量
daily_df = df[~df['date'].isin(['2014-12-11','2014-12-12'])]
view_num = daily_df[daily_df.behavior_type =='1']['behavior_type'].count()
col_num = daily_df[daily_df.behavior_type =='2']['behavior_type'].count()
add_num = daily_df[daily_df.behavior_type =='3']['behavior_type'].count()
buy_num = daily_df[daily_df.behavior_type =='4']['behavior_type'].count()

#日常转化率
view_rate = view_num/view_num
col_rate = col_num/view_num
add_rate = add_num/view_num
buy_rate = buy_num/view_num

#设置漏斗的data_pair参数的list
behavier_labels=['浏览','加购','收藏','购买'] #行为标签
daily_behavier_rate = [np.around(view_rate*100,2), #转化率
                       np.around(add_rate*100,2),
                       np.around(col_rate*100,2),
                       np.around(buy_rate*100,2),]

daily_conversion_rate =(
            Funnel(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
                series_name='用户行为',
                data_pair=[[behavier_labels[i],daily_behavier_rate[i]] for i in range(len(behavier_labels))], #list形式!!!
                gap=4, #漏斗间隔
                tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%",is_show=True), #工具提示的格式设置
                label_opts=opts.LabelOpts(is_show=True, position="ourside")
                )
            .set_global_opts(title_opts=opts.TitleOpts(title="日常用户转化率"))
)
#daily_conversion_rate.render_notebook()
make_snapshot(snapshot, daily_conversion_rate.render(), "daily_conversion_rate.png")

#提取数据
#双12活动各时段行为数量
active_df = df[df['date'].isin(['2014-12-11','2014-12-12'])]
view_active_num = active_df[active_df.behavior_type =='1']['behavior_type'].count()
col_active_num = active_df[active_df.behavior_type =='2']['behavior_type'].count()
add_active_num = active_df[active_df.behavior_type =='3']['behavior_type'].count()
buy_active_num  = active_df[active_df.behavior_type =='4']['behavior_type'].count()

# 活动转化率
view_active_rate = view_active_num/view_active_num
col_active_rate = col_active_num/view_active_num
add_active_rate = add_active_num/view_active_num
buy_active_rate = buy_active_num/view_active_num

#设置漏斗的data_pair参数的list
behavier_labels=['浏览','加购','收藏','购买']
active_behavier_rate =[np.around(view_active_rate*100,2),
                       np.around(add_active_rate*100,2),
                       np.around(col_active_rate*100,2),
                       np.around(buy_active_rate*100,2),]

active_conversion_rate =(
            Funnel(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add(
                series_name='用户行为',
                data_pair=[[behavier_labels[i],active_behavier_rate[i]] for i in range(len(behavier_labels))], #list形式!!!
                gap=4, #漏斗间隔
                tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%",is_show=True),
                label_opts=opts.LabelOpts(is_show=True, position="ourside")
                )
            .set_global_opts(title_opts=opts.TitleOpts(title="双12用户转化率"))
)

#active_conversion_rate.render_notebook()
make_snapshot(snapshot, active_conversion_rate.render(), "active_conversion_rate.png")

#提取数据
#1、流量：类目的pv top10
active_df = df[df['date'].isin(['2014-12-11','2014-12-12'])]
# 降序
view_active_num = active_df[active_df.behavior_type =='1'].groupby('item_category')['behavior_type'].count().sort_values(ascending=False)
# 取前十名
x1= view_active_num.index.tolist()[0:10]
y1=view_active_num.values.tolist()[0:10]

#2、购买增长率：双12类目下单量top10 及其日均下单量增长率 对比
# 双12购买数
active_df = df[df['date'].isin(['2014-12-11','2014-12-12'])]
buy_active_num =active_df[active_df.behavior_type =='4'].groupby('item_category')['behavior_type'].count().reset_index()
#日常购买数
daily_df = df[~df['date'].isin(['2014-12-11','2014-12-12'])]
buy_num = daily_df[daily_df.behavior_type =='4'].groupby('item_category')['behavior_type'].count().reset_index()
#合并
view_buy_avg = buy_active_num.merge(buy_num,how='inner',left_on='item_category',right_on='item_category')
view_buy_avg.columns=['item_category','buy_active_num','buy_num']
#计算增长率
view_buy_avg['buy_active_avg']=view_buy_avg['buy_active_num']/2
view_buy_avg['buy_avg']=view_buy_avg['buy_num']/29
view_buy_avg['growth_rate']=(view_buy_avg['buy_active_avg']-view_buy_avg['buy_avg'])/view_buy_avg['buy_avg']
# 降序
view_buy_avg.sort_values(by=['buy_active_num'],axis=0,ascending=False,inplace=True)
#取前十名
x2=view_buy_avg.item_category.tolist()[0:10]
y2=view_buy_avg.buy_active_num.tolist()[0:10]
y3=np.around(view_buy_avg.growth_rate*100,0).tolist()[0:10]

#制作图表
view_active_bar=(
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(xaxis_data=x1)
    .add_yaxis(
    "pv",
        y1,
        color='rgb(300, 0, 100, 0.2)',
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="双12商品类目pv TOP10"),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        xaxis_opts=opts.AxisOpts(name=' ',name_location = "middle"),
        yaxis_opts=opts.AxisOpts(name='人次',
                                axislabel_opts=opts.LabelOpts(formatter="{value}"))
    )
)

buy_active_bar=(
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(xaxis_data=x2)
    .add_yaxis(
    "下单量",
        y2,
        label_opts=opts.LabelOpts(is_show=False)
                )
     .add_yaxis('日均下单量增长率(与非活动日比较)',
                  yaxis_index=1, 
                  y_axis=y3, 
                  label_opts=opts.LabelOpts(is_show=False) 
                 ) 
      .extend_axis( 
            yaxis=opts.AxisOpts(
                name=' ',
                min_=100,
                max_=600,
                interval=100, 
                axislabel_opts=opts.LabelOpts(formatter="{value}%") 

                                )
                    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="双12商品类目下单量TOP10及日均下单量增长率",pos_top='48%'),
        legend_opts=opts.LegendOpts(pos_top='53%'),
        xaxis_opts=opts.AxisOpts(name='商品类目',name_location = "middle",name_gap=30),
        yaxis_opts=opts.AxisOpts(name=' ',is_show = True,
                                 min_=0,
                                 max_=800, 
                                 interval=200,                                
                                 axislabel_opts=opts.LabelOpts(formatter="{value}"))

                    )
     .set_series_opts(
                    markpoint_opts=opts.MarkPointOpts(data=[ #标记最值！
                        opts.MarkPointItem(type_="min",value_index=1,name="最小值"),
                        opts.MarkPointItem(type_="max",value_index=1,name="最大值")])
                     )
                )

ggrid = (
    Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add(view_active_bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(buy_active_bar, grid_opts=opts.GridOpts(pos_top="60%"))
        )

#ggrid.render_notebook()
make_snapshot(snapshot, ggrid.render(), "ggrid.png")



