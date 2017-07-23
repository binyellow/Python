## xpath：
1. //代表获取很节点
2. /代表获取下层节点
3. selector=etree.HTML(text)
4. pool.map(处理url的函数,urls)
5. 为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:
	- **name**: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
	- **start_urls**: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
	- **parse()** 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。

6. 为了定义常用的输出数据，Scrapy提供了 Item 类。 Item 对象是种简单的容器，保存了爬取到得数据。 其提供了 类似于词典(dictionary-like) 的API以及用于声明可用字段的简单语法。
	- Item使用简单的class定义语法以及Field对象来声明。